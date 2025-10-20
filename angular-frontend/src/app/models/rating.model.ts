export interface ClassDifficultyRequest {
  classCode: string;
  className: string;
  major: string;
  difficultyRating: number;
  professor: string;
  semester: string;
}

export interface ProfessorRatingRequest {
  professor: string;
  classCode: string;
  rating: number;
  review?: string;
  major: string;
  semester: string;
}

export interface ClassRanking {
  classCode: string;
  className: string;
  major: string;
  averageDifficulty: number;
  totalSubmissions: number;
  professors: ProfessorStats[];
}

export interface ProfessorStats {
  name: string;
  avgRating: number;
  ratingCount: number;
}

export interface MajorStats {
  major: string;
  totalClasses: number;
  totalUsers: number;
  averageDifficulty: number;
}
