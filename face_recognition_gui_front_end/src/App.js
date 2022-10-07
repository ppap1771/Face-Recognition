import React, { Component } from "react";
import Webcam from "react-webcam";
import WebCamCapture from './components/WebCam.js'
import './App.css'
import { Apparticle } from "./components/Particle.js";

class App extends Component {
  render() {
    return (
      <div className="container">
        <Apparticle className='particles' />
        <div className="row" >
          <h2 className="heading" >  Live face recognition </h2>
          <WebCamCapture />
        </div>

      </div>
    );
  }
}

export default App;
