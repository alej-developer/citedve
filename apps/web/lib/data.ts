import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import type { LatestDocument, SignalsDocument, Signal } from "@radar/schema";

const ROOT = path.resolve(process.cwd(), "..", "..");
const DATA_DIR = path.join(ROOT, "data");
const CONTENT_DIR = path.join(ROOT, "content", "radar");

export function loadLatest(): LatestDocument {
  try {
    const file = path.join(DATA_DIR, "latest.json");
    return JSON.parse(fs.readFileSync(file, "utf-8")) as LatestDocument;
  } catch {
    return { schema_version: "0.1.0", edition: null, signals: [] };
  }
}

export function loadAllSignals(): Signal[] {
  try {
    const file = path.join(DATA_DIR, "signals.json");
    const doc = JSON.parse(fs.readFileSync(file, "utf-8")) as SignalsDocument;
    return doc.signals;
  } catch {
    return [];
  }
}

export function getSignalById(id: string): Signal | undefined {
  return loadAllSignals().find(s => s.id === id);
}

export interface RadarPost {
  slug: string;
  title: string;
  content: string;
  edition: string;
}

export function getRadarPosts(): Omit<RadarPost, "content">[] {
  if (!fs.existsSync(CONTENT_DIR)) return [];
  
  const files = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith(".md") && !f.startsWith("_") && f !== "README.md");
  const posts = files.map(file => {
    const filePath = path.join(CONTENT_DIR, file);
    const source = fs.readFileSync(filePath, "utf-8");
    const { data } = matter(source);
    return {
      slug: file.replace(".md", ""),
      title: data.title || `Semana del ${file.replace(".md", "")}`,
      edition: data.edition || file.replace(".md", ""),
    };
  });
  
  return posts.sort((a, b) => (a.edition > b.edition ? -1 : 1));
}

export function getRadarPost(slug: string): RadarPost | null {
  const filePath = path.join(CONTENT_DIR, `${slug}.md`);
  if (!fs.existsSync(filePath)) return null;
  
  const source = fs.readFileSync(filePath, "utf-8");
  const { data, content } = matter(source);
  
  return {
    slug,
    title: data.title || `Semana del ${slug}`,
    edition: data.edition || slug,
    content,
  };
}
