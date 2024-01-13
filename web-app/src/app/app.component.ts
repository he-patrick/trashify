import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import {WebcamComponent} from './webcam/webcam.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, WebcamComponent],
  template: `
  <div>
    <webcam
      [trigger]="trigger"
      [width]="640"
      [height]="480"
      [videoOptions]="videoOptions"
      (imageCapture)="handleImage($event)">
    </webcam>
  </div>
  
  <button (click)="triggerSnapshot()">Take Picture</button>
  `,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'web-app';
}
