import { create } from "zustand";
import type { LearningPath, StageWithStatus, ContentItem } from "@/lib/api";

interface LearningState {
  // Data
  learningPath: LearningPath | null;
  currentStage: StageWithStatus | null;
  currentContent: ContentItem[];

  // Loading states
  isLoading: boolean;
  error: string | null;

  // Actions
  setLearningPath: (path: LearningPath) => void;
  setCurrentStage: (stage: StageWithStatus | null) => void;
  setCurrentContent: (content: ContentItem[]) => void;
  markContentComplete: (contentId: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  learningPath: null,
  currentStage: null,
  currentContent: [],
  isLoading: false,
  error: null,
};

export const useLearningStore = create<LearningState>((set) => ({
  ...initialState,

  setLearningPath: (path) =>
    set({
      learningPath: path,
      currentStage: path.current_stage,
    }),

  setCurrentStage: (stage) => set({ currentStage: stage }),

  setCurrentContent: (content) => set({ currentContent: content }),

  markContentComplete: (contentId) =>
    set((state) => ({
      currentContent: state.currentContent.map((item) =>
        item.id === contentId ? { ...item, is_completed: true } : item
      ),
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  reset: () => set(initialState),
}));
