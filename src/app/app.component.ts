import { Component } from '@angular/core';
import { FormBuilder,FormGroup } from '@angular/forms';
import { WebcamImage } from 'ngx-webcam';
import { Observable, Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  constructor(private http : HttpClient) { }

  stream: any = null;
  status: any = null;
  trigger: Subject<void> = new Subject();
  previewImage: string = '';
  btnLabel: string = 'Capture image';

  get $trigger(): Observable<void> {
    return this.trigger.asObservable();
  }

  snapshot(event: WebcamImage) {
    this.image=event
    console.log(event);
    this.previewImage = event.imageAsDataUrl;
    this.btnLabel = 'Re capture image'
  }
  checkPermissions() {
    navigator.mediaDevices.getUserMedia({
      video: {
        width: 500,
        height: 500
      }
    }).then((res) => {
      console.log("response", res);
      this.stream = res;
      this.status = 'My camera is accessing';
      this.btnLabel = 'Capture image';
    }).catch(err => {
      console.log(err);
      if(err?.message === 'Permission denied') {
        this.status = 'Permission denied please try again by approving the access';
      } else {
        this.status = 'You may not having camera system, Please try again ...';
      }
    })
  }

  captureImage() {
    this.trigger.next();
  }

  proceed() {
    //console.log(this.previewImage);
    this.downloadAndUploadImage(this.previewImage)
  }

  data:any
  image:any

  //formData:any = new FormData()
  //formData.append('emoji',this.previewImage)
  

  onHttpgetData(imageData:any){
    const formData: FormData = new FormData();
    formData.append('emoji', this.image); 
    this.http.post("http://127.0.0.1:5000/",imageData)
    .subscribe((data)=>{
      if(this.data=data)
        window.open("https://www.youtube.com/results?search_query="+data)
      else
        console.log("mistake")
  })
  }

  fetchImage(src: string): Observable<Blob> {
    return this.http.get(src, { responseType: 'blob' });
  }
  private blobToFile(blob: Blob, fileName: string): File {
    const file: File = new File([blob], fileName, { type: blob.type });
    return file;
  }
  uploadImage(file: File) {
    const formData = new FormData();
    formData.append('emoji', file, file.name);
    this.onHttpgetData(formData)
  }
  
  downloadAndUploadImage(src: string): void {
    this.fetchImage(src).subscribe(blob => {
      const file = this.blobToFile(blob, 'filename.jpg');
      this.uploadImage(file)
    });
  }
    
  

}
