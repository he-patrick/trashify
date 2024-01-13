// webcam.component.ts
import { Component, OnInit, ViewChild } from '@angular/core';
import { WebcamImage, WebcamInitError, WebcamUtil } from 'ngx-webcam';
import { Subject, Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './webcam.component.html',
  styleUrls: ['./webcam.component.css']
})
export class WebcamComponent implements OnInit {
  @ViewChild('webcam') webcamElement: any;

  private trigger: Subject<void> = new Subject<void>();
  public webcamImage: WebcamImage | undefined;

  ngOnInit(): void {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        console.log(mediaDevices);
      });

    this.startWebcam();
  }

  public triggerSnapshot(): void {
    this.trigger.next();
  }

  public handleImage(webcamImage: WebcamImage): void {
    console.info('Received webcam image', webcamImage);
    // Save the image or pass it to another service
    this.webcamImage = webcamImage;
  }

  private startWebcam(): void {
    this.webcamElement.start();
  }
}
