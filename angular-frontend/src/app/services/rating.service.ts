import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  ClassDifficultyRequest,
  ProfessorRatingRequest,
  ClassRanking,
  MajorStats
} from '../models/rating.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RatingService {
  private http = inject(HttpClient);

  getAllMajors(): Observable<string[]> {
    return this.http.get<string[]>(`${environment.apiUrl}/majors`);
  }

  getMajorStats(major: string): Observable<MajorStats> {
    return this.http.get<MajorStats>(`${environment.apiUrl}/majors/${major}/stats`);
  }

  getClassRankings(major: string, limit: number = 50): Observable<ClassRanking[]> {
    return this.http.get<ClassRanking[]>(
      `${environment.apiUrl}/majors/${major}/classes?limit=${limit}`
    );
  }

  submitClassDifficulty(request: ClassDifficultyRequest): Observable<any> {
    return this.http.post(`${environment.apiUrl}/submissions/difficulty`, request);
  }

  submitProfessorRating(request: ProfessorRatingRequest): Observable<any> {
    return this.http.post(`${environment.apiUrl}/submissions/professor`, request);
  }

  getProfessorRatings(professor: string, classCode?: string): Observable<any> {
    const params = classCode ? `?classCode=${classCode}` : '';
    return this.http.get(`${environment.apiUrl}/professors/${professor}/ratings${params}`);
  }
}
