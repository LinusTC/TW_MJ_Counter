import { SupportedLanguage } from "@/language_constants";

export interface UserSettings {
    name: string;
    theme?: "light" | "dark" | "auto";
    language?: SupportedLanguage;
    profilePic?: string;
}

export interface ScoringRules {
    id: number;
    name: string;
    rules: Record<string, number>;
    is_default: boolean;
    created_at: string;
}
