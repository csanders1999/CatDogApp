import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(private http: HttpService) { }

  analysis: any
  personalityChart: Chart
  attributes: string[]

  ngOnInit() {
    this.analysis = this.http.analysis
    this.attributes = Object.keys(this.analysis.personality)
    var chartElement = <HTMLCanvasElement> document.getElementById('personalityChart');
    this.personalityChart = new Chart(chartElement.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Openness', 'Conscientiousness', 'Agreeableness', 'Emotional Range', 'Extraversion'],
        datasets: [
          {
            data: [
              this.analysis.cat_dog_personality.big5_openness[0],
              this.analysis.cat_dog_personality.big5_conscientiousness[0],
              this.analysis.cat_dog_personality.big5_agreeableness[0],
              this.analysis.cat_dog_personality.big5_emotional_range[0],
              this.analysis.cat_dog_personality.big5_extraversion[0]
              ],
            backgroundColor: [
              'rgba(63, 63, 191, 0.2)',
              'rgba(63, 63, 191, 0.2)',
              'rgba(63, 63, 191, 0.2)',
              'rgba(63, 63, 191, 0.2)',
              'rgba(63, 63, 191, 0.2)',
            ],
            borderColor: [
              'rgba(63, 63, 191, 1)',
              'rgba(63, 63, 191, 1)',
              'rgba(63, 63, 191, 1)',
              'rgba(63, 63, 191, 1)',
              'rgba(63, 63, 191, 1)',
            ],
            borderWidth: 1,
            label: 'Dog Lovers'
          },
          {
            data: [this.analysis.personality.big5_openness,
                  this.analysis.personality.big5_conscientiousness,
                  this.analysis.personality.big5_agreeableness,
                  this.analysis.personality.big5_emotional_range,
                  this.analysis.personality.big5_extraversion],
            backgroundColor: [
              'rgba(63, 191, 191, 0.2)',
              'rgba(63, 191, 191, 0.2)',
              'rgba(63, 191, 191, 0.2)',
              'rgba(63, 191, 191, 0.2)',
              'rgba(63, 191, 191, 0.2)',
            ],
            borderColor: [
              'rgba(63, 191, 191, 1)',
              'rgba(63, 191, 191, 1)',
              'rgba(63, 191, 191, 1)',
              'rgba(63, 191, 191, 1)',
              'rgba(63, 191, 191, 1)',
            ],
            borderWidth: 1,
            label: this.analysis.username
          },
          {
            data: [this.analysis.cat_dog_personality.big5_openness[1],
                  this.analysis.cat_dog_personality.big5_conscientiousness[1],
                  this.analysis.cat_dog_personality.big5_agreeableness[1],
                  this.analysis.cat_dog_personality.big5_emotional_range[1],
                  this.analysis.cat_dog_personality.big5_extraversion[1]],
            backgroundColor: [
              'rgba(191, 63, 191, 0.2)',
              'rgba(191, 63, 191, 0.2)',
              'rgba(191, 63, 191, 0.2)',
              'rgba(191, 63, 191, 0.2)',
              'rgba(191, 63, 191, 0.2)',
            ],
            borderColor: [
              'rgba(191, 63, 191, 1)',
              'rgba(191, 63, 191, 1)',
              'rgba(191, 63, 191, 1)',
              'rgba(191, 63, 191, 1)',
              'rgba(191, 63, 191, 1)',
            ],
            borderWidth: 1,
            label: 'Cat Lovers'
          }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    })
    console.log(this.personalityChart)
  }



}
