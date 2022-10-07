import React, { useState } from 'react'
import axios from 'axios'
import WebCam from 'react-webcam'
import '../styles/webcam.css'
const URL = "http://127.0.0.1:5000/"
const WebCamCapture = () => {
    const webcamRef = React.useRef(null);
    const videoConstraints = {
        width: 800,
        height: 800,
        faceingMode: 'user'
    };
    const [name, setName] = useState("")
    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(`imageSrc = ${imageSrc}`)
        axios.post(`${URL}api` , {data : imageSrc}).then(res=>{
            console.log(`response is ${res}`)
            setName(res.data)
        })
    }
    , 
    [webcamRef]
    )

return (
    <div className='webcam-container'>
        <WebCam audio = {false} heigrht = {300}  ref = {webcamRef} 
        screenshotFormat= "image/jpeg"
        width={350} 
        videoConstraints = {videoConstraints}
         />  
         <br/>

        <button className='webcam-btn btn btn-primary' onClick={capture} > CLICK ME   </button>
        <br />

        <h2 className='webcam-name' >{name} </h2>

    </div>
)


}

export default WebCamCapture