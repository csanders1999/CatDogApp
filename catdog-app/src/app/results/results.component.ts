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
  catScore: number
  dogScore: number

  ngOnInit() {
    // Get analysis object from http service
    this.analysis = this.http.analysis

    // Put personality attribute names into a list for usage in HTML template
    this.attributes = Object.keys(this.analysis.personality)

    // Calculate the user's final cat and dog score
    // The score is calculated by converting all metrics (sentiment analysis score, images posted,
    // and personality analysis) to a 0 to 1 scale and summing them for a maximum possible total of 3.
    // If desired, certain metrics may be weighted to reflect more or less significance.
    // Please see the report for a detailed description of each term's meaning
    let dogCatPersonality = this.analysis.cat_dog_personality
    this.catScore = 
      (this.analysis.cat_num + this.analysis.cat_sa_score)/(this.analysis.cat_num*2) + 
      (this.analysis.cat_img_num / 60) +
      (1 - 
        (Math.abs(this.analysis.personality.big5_agreeableness - dogCatPersonality.big5_agreeableness[1]) +
         Math.abs(this.analysis.personality.big5_openness - dogCatPersonality.big5_openness[1]) +
         Math.abs(this.analysis.personality.big5_conscientiousness - dogCatPersonality.big5_conscientiousness[1]) +
         Math.abs(this.analysis.personality.big5_emotional_range - dogCatPersonality.big5_emotional_range[1]) +
         Math.abs(this.analysis.personality.big5_extraversion - dogCatPersonality.big5_extraversion[1]))
      )

    this.dogScore = 
    (this.analysis.dog_num + this.analysis.dog_sa_score)/(this.analysis.dog_num*2) +
    (this.analysis.dog_img_num / 60) +
    (1 - 
      (Math.abs(this.analysis.personality.big5_agreeableness - dogCatPersonality.big5_agreeableness[0]) +
        Math.abs(this.analysis.personality.big5_openness - dogCatPersonality.big5_openness[0]) +
        Math.abs(this.analysis.personality.big5_conscientiousness - dogCatPersonality.big5_conscientiousness[0]) +
        Math.abs(this.analysis.personality.big5_emotional_range - dogCatPersonality.big5_emotional_range[0]) +
        Math.abs(this.analysis.personality.big5_extraversion - dogCatPersonality.big5_extraversion[0]))
    )

    console.log(this.catScore)
    console.log(this.dogScore)

    if (isNaN(this.dogScore)) {
      this.dogScore = 0
    }
    if (isNaN(this.catScore)) {
      this.catScore = 0
    }

    // Create graph
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
  }



}
