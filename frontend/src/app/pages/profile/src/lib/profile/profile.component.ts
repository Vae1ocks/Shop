import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'lib-profile',
  standalone: true,
  imports: [RouterOutlet, CommonModule, RouterLink],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
})

export class ProfileComponent implements OnInit {
 public link = ''
  constructor() {
  }

  ngOnInit() {

  }


}
