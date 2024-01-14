'use client'

import React from 'react';
import WebcamCapture from '../components/webcam'

const Home: React.FC = () => {
    return (
        <div>
            <h1>Webcam Capture</h1>
            <WebcamCapture />
        </div>
    );
};

export default Home;