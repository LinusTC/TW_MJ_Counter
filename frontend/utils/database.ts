import * as SQLite from "expo-sqlite";
import * as defaultValues from "@/constants/values";

const db = SQLite.openDatabaseSync("twmj.db");

export function initDb() {
    db.execSync(`
    CREATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS scoring_templates (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      rules TEXT NOT NULL,
      is_default INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

    const existingRules = db.getFirstSync(
        "SELECT COUNT(*) as count FROM scoring_templates"
    );
    if ((existingRules as any).count === 0) {
        saveScoringTemplate("Default Taiwan Rules", defaultValues, true);
    }
}

// Settings operations
export function saveSetting(key: string, value: string) {
    db.runSync("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", [
        key,
        value,
    ]);
}

export function getSetting(key: string, defaultValue: string = "SET A NAME") {
    const result = db.getFirstSync("SELECT value FROM settings WHERE key = ?", [
        key,
    ]);
    return result ? (result as any).value : defaultValue;
}

// Scoring rules operations
export function saveScoringTemplate(
    name: string,
    rules: object,
    isDefault: boolean = false
) {
    // If setting as default, unset other defaults first
    if (isDefault) {
        db.runSync("UPDATE scoring_templates SET is_default = 0");
    }

    const stmt = db.prepareSync(
        "INSERT INTO scoring_templates (name, rules, is_default) VALUES (?, ?, ?)"
    );
    stmt.executeSync([name, JSON.stringify(rules), isDefault ? 1 : 0]);
}

export function getScoringTemplates() {
    const result = db.getAllSync(
        "SELECT * FROM scoring_templates ORDER BY is_default DESC, created_at DESC"
    );
    return result.map((row: any) => ({
        ...row,
        rules: JSON.parse(row.rules),
        is_default: row.is_default === 1,
    }));
}

export function getDefaultScoringTemplate() {
    const result = db.getFirstSync(
        "SELECT * FROM scoring_templates WHERE is_default = 1"
    );
    if (result) {
        return {
            ...(result as any),
            rules: JSON.parse((result as any).rules),
            is_default: true,
        };
    }
    return null;
}

export function updateScoringTemplate(id: number, name: string, rules: object) {
    db.runSync(
        "UPDATE scoring_templates SET name = ?, rules = ? WHERE id = ?",
        [name, JSON.stringify(rules), id]
    );
}

export function setDefaultScoringTemplate(id: number) {
    db.execSync(`
    UPDATE scoring_templates SET is_default = 0;
    UPDATE scoring_templates SET is_default = 1 WHERE id = ${id};
  `);
}

export function deleteScoringTemplate(id: number) {
    db.runSync("DELETE FROM scoring_templates WHERE id = ?", [id]);
}

//FOR TESTING ONLY PLEASE REMOVE WHEN DEPLOY
export function resetDatabase() {
    db.execSync(`
    DROP TABLE IF EXISTS settings;
    DROP TABLE IF EXISTS scoring_templates;
  `);
    initDb();
}
