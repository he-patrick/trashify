import React, { useRef, useState, useEffect } from 'react';

const WebcamCapture: React.FC = () => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [image, setImage] = useState<string>('');

    useEffect(() => {
        getVideoStream();
    }, []);

    const getVideoStream = () => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            })
            .catch(err => console.error("Error accessing the camera: ", err));
    };

    const captureImage = () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        if (video && canvas) {
            const context = canvas.getContext('2d');
            context?.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL('image/png');
            setImage(imageData);
            uploadImage(imageData);
    
        }
    };

    const uploadImage = async (imageData: string) => {
        try {
            // Convert the base64 string to a file-like object
            const blob = await fetch(imageData).then(r => r.blob());
            const formData = new FormData();
            formData.append('image', blob, 'captured_image.png');
  
            const response = await fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: formData // Send formData here
            });
            const data = await response.json();
        } catch (error) {
            console.error("Error uploading the image: ", error);
        }
      };
  
      return (
          <div>
              <video ref={videoRef} width="640" height="480" autoPlay />
              <button onClick={captureImage}>Capture</button>
              <canvas ref={canvasRef} width="640" height="480" style={{ display: 'none' }} />
              {image && <img src={image} alt="Captured" />}
              
          </div>
      );
  };
  
  export default WebcamCapture;