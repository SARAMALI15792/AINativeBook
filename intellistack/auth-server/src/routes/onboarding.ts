/**
 * Onboarding API Routes
 * Handles 4-step onboarding flow for new users
 */

import { Router } from 'express';
import { auth } from '../auth.js';
import { db } from '../db.js';
import { user as userTable } from '../auth-schema.js';
import { eq } from 'drizzle-orm';

const router = Router();

/**
 * Validation schemas for each onboarding step
 */
const validateBasicInfo = (data: any): { valid: boolean; error?: string } => {
  if (!data.full_name || typeof data.full_name !== 'string' || data.full_name.trim().length === 0) {
    return { valid: false, error: 'Full name is required' };
  }
  if (!data.preferred_language || !['en', 'ur'].includes(data.preferred_language)) {
    return { valid: false, error: 'Preferred language must be "en" or "ur"' };
  }
  if (!data.timezone || typeof data.timezone !== 'string') {
    return { valid: false, error: 'Timezone is required' };
  }
  return { valid: true };
};

const validateEducation = (data: any): { valid: boolean; error?: string } => {
  const validLevels = ['high_school', 'undergraduate', 'graduate', 'professional'];
  if (!data.level || !validLevels.includes(data.level)) {
    return { valid: false, error: 'Education level must be one of: high_school, undergraduate, graduate, professional' };
  }
  if (!data.field_of_study || typeof data.field_of_study !== 'string' || data.field_of_study.trim().length === 0) {
    return { valid: false, error: 'Field of study is required' };
  }
  const validExperience = ['none', 'beginner', 'intermediate', 'advanced'];
  if (!data.prior_experience || !validExperience.includes(data.prior_experience)) {
    return { valid: false, error: 'Prior experience must be one of: none, beginner, intermediate, advanced' };
  }
  return { valid: true };
};

const validateInterests = (data: any): { valid: boolean; error?: string } => {
  const validGoals = ['career_change', 'academic_research', 'hobby', 'professional_development'];
  if (!Array.isArray(data.learning_goals) || data.learning_goals.length === 0) {
    return { valid: false, error: 'At least one learning goal is required' };
  }
  if (!data.learning_goals.every((goal: string) => validGoals.includes(goal))) {
    return { valid: false, error: 'Invalid learning goal' };
  }

  const validStyles = ['visual', 'reading', 'hands_on', 'mixed'];
  if (!data.learning_style || !validStyles.includes(data.learning_style)) {
    return { valid: false, error: 'Learning style must be one of: visual, reading, hands_on, mixed' };
  }

  const validTopics = ['ros2', 'simulation', 'perception', 'ai_integration', 'hardware'];
  if (!Array.isArray(data.topics_of_interest) || data.topics_of_interest.length === 0) {
    return { valid: false, error: 'At least one topic of interest is required' };
  }
  if (!data.topics_of_interest.every((topic: string) => validTopics.includes(topic))) {
    return { valid: false, error: 'Invalid topic of interest' };
  }

  return { valid: true };
};

const validateAdditional = (data: any): { valid: boolean; error?: string } => {
  // All fields are optional
  if (data.linkedin_url && typeof data.linkedin_url === 'string') {
    // Basic URL validation
    try {
      new URL(data.linkedin_url);
    } catch {
      return { valid: false, error: 'Invalid LinkedIn URL format' };
    }
  }

  if (data.bio && typeof data.bio === 'string' && data.bio.length > 500) {
    return { valid: false, error: 'Bio must be 500 characters or less' };
  }

  return { valid: true };
};

/**
 * GET /api/auth/onboarding/status
 * Get user's onboarding completion status and current step
 */
router.get('/status', async (req, res) => {
  try {
    const session = await auth.api.getSession({ headers: req.headers as any });

    if (!session) {
      return res.status(401).json({ error: 'UNAUTHORIZED', message: 'No valid session found' });
    }

    // Fetch current user data from database
    const currentUser = await db
      .select()
      .from(userTable)
      .where(eq(userTable.id, session.user.id))
      .limit(1);

    if (!currentUser[0]) {
      return res.status(404).json({ error: 'USER_NOT_FOUND', message: 'User not found' });
    }

    const user = currentUser[0];
    const preferences = (user.preferences as any) || {};

    const completedSteps: string[] = [];
    if (preferences.basic_info) completedSteps.push('basic_info');
    if (preferences.education) completedSteps.push('education');
    if (preferences.interests) completedSteps.push('interests');
    if (preferences.additional) completedSteps.push('additional');

    const currentStep = completedSteps.length + 1;

    return res.json({
      onboarding_completed: user.onboarding_completed || false,
      current_step: currentStep > 4 ? 4 : currentStep,
      completed_steps: completedSteps,
      preferences,
    });
  } catch (error: any) {
    console.error('Error getting onboarding status:', error);
    return res.status(500).json({ error: 'SERVER_ERROR', message: 'Failed to get onboarding status' });
  }
});

/**
 * POST /api/auth/onboarding/step
 * Save data for a specific onboarding step
 */
router.post('/step', async (req, res) => {
  try {
    const session = await auth.api.getSession({ headers: req.headers as any });

    if (!session) {
      return res.status(401).json({ error: 'UNAUTHORIZED', message: 'No valid session found' });
    }

    const { step, data } = req.body;

    if (!step || !data) {
      return res.status(400).json({ error: 'VALIDATION_ERROR', message: 'Step and data are required' });
    }

    // Validate step data based on step type
    let validation: { valid: boolean; error?: string };
    switch (step) {
      case 'basic_info':
        validation = validateBasicInfo(data);
        break;
      case 'education':
        validation = validateEducation(data);
        break;
      case 'interests':
        validation = validateInterests(data);
        break;
      case 'additional':
        validation = validateAdditional(data);
        break;
      default:
        return res.status(400).json({ error: 'VALIDATION_ERROR', message: 'Invalid step name' });
    }

    if (!validation.valid) {
      return res.status(400).json({ error: 'VALIDATION_ERROR', message: validation.error });
    }

    // Fetch current preferences from database
    const currentUser = await db
      .select()
      .from(userTable)
      .where(eq(userTable.id, session.user.id))
      .limit(1);

    const currentPreferences = (currentUser[0]?.preferences as any) || {};
    const updatedPreferences = {
      ...currentPreferences,
      [step]: data,
    };

    // Update user preferences in database
    await db
      .update(userTable)
      .set({ preferences: updatedPreferences })
      .where(eq(userTable.id, session.user.id));

    // Determine next step
    const stepOrder = ['basic_info', 'education', 'interests', 'additional'];
    const currentIndex = stepOrder.indexOf(step);
    const nextStep = currentIndex < stepOrder.length - 1 ? stepOrder[currentIndex + 1] : null;

    // Check if all steps are complete
    const allStepsComplete =
      updatedPreferences.basic_info &&
      updatedPreferences.education &&
      updatedPreferences.interests &&
      updatedPreferences.additional;

    return res.json({
      success: true,
      onboarding_completed: allStepsComplete,
      next_step: nextStep,
    });
  } catch (error: any) {
    console.error('Error saving onboarding step:', error);
    return res.status(500).json({ error: 'SERVER_ERROR', message: 'Failed to save onboarding step' });
  }
});

/**
 * POST /api/auth/onboarding/complete
 * Mark onboarding as complete after all steps are done
 */
router.post('/complete', async (req, res) => {
  try {
    const session = await auth.api.getSession({ headers: req.headers as any });

    if (!session) {
      return res.status(401).json({ error: 'UNAUTHORIZED', message: 'No valid session found' });
    }

    // Fetch current user data from database
    const currentUser = await db
      .select()
      .from(userTable)
      .where(eq(userTable.id, session.user.id))
      .limit(1);

    if (!currentUser[0]) {
      return res.status(404).json({ error: 'USER_NOT_FOUND', message: 'User not found' });
    }

    const preferences = (currentUser[0].preferences as any) || {};

    // Verify all steps are complete
    const allStepsComplete =
      preferences.basic_info &&
      preferences.education &&
      preferences.interests &&
      preferences.additional;

    if (!allStepsComplete) {
      const missingSteps: string[] = [];
      if (!preferences.basic_info) missingSteps.push('basic_info');
      if (!preferences.education) missingSteps.push('education');
      if (!preferences.interests) missingSteps.push('interests');
      if (!preferences.additional) missingSteps.push('additional');

      return res.status(400).json({
        error: 'INCOMPLETE_ONBOARDING',
        message: 'All onboarding steps must be completed',
        missing_steps: missingSteps,
      });
    }

    // Mark onboarding as complete
    await db
      .update(userTable)
      .set({ onboarding_completed: true })
      .where(eq(userTable.id, session.user.id));

    return res.json({
      success: true,
      user: {
        id: session.user.id,
        onboarding_completed: true,
        current_stage: 1,
      },
    });
  } catch (error: any) {
    console.error('Error completing onboarding:', error);
    return res.status(500).json({ error: 'SERVER_ERROR', message: 'Failed to complete onboarding' });
  }
});

export default router;
