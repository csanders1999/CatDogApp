import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {
  constructor(private router: Router, private http: HttpService) { }

  showError: boolean = false // Flag for showing empty field error
  loading: boolean = false // Flag for showing loading gif

  ngOnInit() {
  }

  // Check that a username has been entered, then send the username for analysis
  // When the analysis is given  back, update the analysis object in http service and 
  // go to results page
  analyzeUser(username: string) {
    if (username == "") {
      this.showError = true;
    }
    else {
      this.loading = true
      this.showError = false
      this.http.postUsername(username)
        .subscribe(response => {
          console.log(response)
          this.http.analysis = response
          this.router.navigate(['results'])
        })
    }
  }

}
