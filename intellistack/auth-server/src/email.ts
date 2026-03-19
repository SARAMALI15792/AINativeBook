/**
 * Email Service Configuration
 * Uses Resend API for sending verification and password reset emails
 */

import { Resend } from 'resend';

// Initialize Resend client
const resend = new Resend(process.env.RESEND_API_KEY);

const FROM_EMAIL = process.env.EMAIL_FROM || 'noreply@intellistack.dev';
const SUPPORT_EMAIL = process.env.SUPPORT_EMAIL || 'support@intellistack.dev';
const APP_URL = process.env.BETTER_AUTH_URL || 'http://localhost:3001';

/**
 * Send verification email
 */
export async function sendVerificationEmail(email: string, verificationToken: string): Promise<void> {
  const verificationUrl = `${APP_URL}/verify-email?token=${verificationToken}`;

  const htmlContent = `
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
      .container { max-width: 600px; margin: 0 auto; padding: 20px; }
      .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
      .button { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0; }
      .footer { border-top: 1px solid #eee; padding-top: 20px; margin-top: 40px; font-size: 12px; color: #666; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Welcome to IntelliStack! 🎓</h1>
      </div>

      <p>Hi there,</p>

      <p>Thank you for signing up! To activate your account, please verify your email address by clicking the button below:</p>

      <a href="${verificationUrl}" class="button">Verify Email Address</a>

      <p>Or copy and paste this link in your browser:</p>
      <p style="word-break: break-all; background: #f5f5f5; padding: 10px; border-radius: 4px;">${verificationUrl}</p>

      <p>This link will expire in 24 hours.</p>

      <p>If you didn't create this account, you can safely ignore this email.</p>

      <div class="footer">
        <p>© 2026 IntelliStack Platform. All rights reserved.</p>
        <p>Need help? Contact us at <a href="mailto:${SUPPORT_EMAIL}">${SUPPORT_EMAIL}</a></p>
      </div>
    </div>
  </body>
</html>
  `;

  try {
    await resend.emails.send({
      from: FROM_EMAIL,
      to: email,
      subject: 'Verify your IntelliStack account',
      html: htmlContent,
    });
    console.log(`✉️  Verification email sent to ${email}`);
  } catch (error) {
    console.error('Failed to send verification email:', error);
    throw new Error('Failed to send verification email');
  }
}

/**
 * Send password reset email
 */
export async function sendPasswordResetEmail(email: string, resetToken: string): Promise<void> {
  const resetUrl = `${APP_URL}/reset-password?token=${resetToken}`;

  const htmlContent = `
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
      .container { max-width: 600px; margin: 0 auto; padding: 20px; }
      .alert { background: #fef3cd; border: 1px solid #ffc107; color: #856404; padding: 12px; border-radius: 4px; margin: 20px 0; }
      .button { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0; }
      .footer { border-top: 1px solid #eee; padding-top: 20px; margin-top: 40px; font-size: 12px; color: #666; }
    </style>
  </head>
  <body>
    <div class="container">
      <h2>Password Reset Request</h2>

      <p>We received a request to reset your IntelliStack password. Click the button below to create a new password:</p>

      <a href="${resetUrl}" class="button">Reset Password</a>

      <p>Or copy and paste this link in your browser:</p>
      <p style="word-break: break-all; background: #f5f5f5; padding: 10px; border-radius: 4px;">${resetUrl}</p>

      <div class="alert">
        ⚠️ <strong>This link will expire in 1 hour.</strong>
      </div>

      <p><strong>Didn't request this?</strong></p>
      <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>

      <p>For security reasons, never share this link with anyone.</p>

      <div class="footer">
        <p>© 2026 IntelliStack Platform. All rights reserved.</p>
        <p>Need help? Contact us at <a href="mailto:${SUPPORT_EMAIL}">${SUPPORT_EMAIL}</a></p>
      </div>
    </div>
  </body>
</html>
  `;

  try {
    await resend.emails.send({
      from: FROM_EMAIL,
      to: email,
      subject: 'Reset your IntelliStack password',
      html: htmlContent,
    });
    console.log(`✉️  Password reset email sent to ${email}`);
  } catch (error) {
    console.error('Failed to send password reset email:', error);
    throw new Error('Failed to send password reset email');
  }
}

/**
 * Send welcome email for new users
 */
export async function sendWelcomeEmail(email: string, name: string): Promise<void> {
  const htmlContent = `
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
      .container { max-width: 600px; margin: 0 auto; padding: 20px; }
      .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
      .features { margin: 30px 0; }
      .feature { margin: 15px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #667eea; }
      .button { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0; }
      .footer { border-top: 1px solid #eee; padding-top: 20px; margin-top: 40px; font-size: 12px; color: #666; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Welcome to IntelliStack! 🚀</h1>
        <p>Your journey in Physical AI learning starts here.</p>
      </div>

      <p>Hi ${name},</p>

      <p>Your IntelliStack account is all set! Here's what you can do:</p>

      <div class="features">
        <div class="feature">
          <strong>📚 Progressive Learning Path</strong> - Learn through 5 stages: Foundations, ROS 2 & Simulation, Perception & Planning, AI Integration, and Capstone
        </div>
        <div class="feature">
          <strong>🤖 AI Tutor</strong> - Get personalized help with Socratic-style guidance while learning
        </div>
        <div class="feature">
          <strong>💻 Hands-on Projects</strong> - Practice with simulation environments and real-world robotics challenges
        </div>
        <div class="feature">
          <strong>🏆 Gamification</strong> - Earn badges and certificates as you progress through the curriculum
        </div>
      </div>

      <a href="${APP_URL}/dashboard" class="button">Go to Dashboard</a>

      <p>If you have any questions, feel free to reach out to us at <a href="mailto:${SUPPORT_EMAIL}">${SUPPORT_EMAIL}</a></p>

      <div class="footer">
        <p>© 2026 IntelliStack Platform. All rights reserved.</p>
      </div>
    </div>
  </body>
</html>
  `;

  try {
    await resend.emails.send({
      from: FROM_EMAIL,
      to: email,
      subject: `Welcome to IntelliStack, ${name}!`,
      html: htmlContent,
    });
    console.log(`✉️  Welcome email sent to ${email}`);
  } catch (error) {
    console.error('Failed to send welcome email:', error);
    // Don't throw - welcome email is not critical
  }
}
