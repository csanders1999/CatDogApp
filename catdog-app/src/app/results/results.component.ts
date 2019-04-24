import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(private http: HttpService) { }

  analysis: any

  ngOnInit() {
    this.analysis = this.http.analysis
  }

  

}
