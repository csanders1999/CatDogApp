import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  analysis: any // Analysis object returned from python scripts
  httpOptions = { 
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(private http: HttpClient) { }

  // Send username to node and wait for analysis to be sent back to observable
  postUsername(username: string): Observable<any> {
    return this.http.post('http://localhost:4000/user', JSON.stringify({ user: username }), this.httpOptions)
  }
}
