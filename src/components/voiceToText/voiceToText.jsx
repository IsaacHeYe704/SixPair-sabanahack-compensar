import { useEffect, useRef, useState } from "react";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import microPhoneIcon from "../../assets/microphone.png";
import "./voice.css"
const VoiceToText = ({talktToVivi,setEscribiendo}) => {
    const {
      transcript,
      listening,
      resetTranscript,
      browserSupportsSpeechRecognition
    } = useSpeechRecognition();
    const [isListening, setIsListening] = useState(false);
    const microphoneRef = useRef(null);
    if (!browserSupportsSpeechRecognition) {
      return <span>Browser doesn't support speech recognition.</span>;
    }
    useEffect(() => {
        setEscribiendo(listening)
    }, [listening])

    const handleListing = () => {
      setIsListening(true);
      microphoneRef.current.classList.add("listening");
      SpeechRecognition.startListening({
        continuous: true,
      });
    };
    const stopHandle = () => {
      setIsListening(false);
      microphoneRef.current.classList.remove("listening");
      SpeechRecognition.stopListening();
    };
    const handleReset = () => {
        setIsListening(false);
      stopHandle();
      resetTranscript();
      resetTranscript();
    };
    const sendData = () => {
        handleReset()
        resetTranscript();
        talktToVivi(transcript)
    }
  return (
    <div className="microphone-wrapper">
        {transcript  && (
        <div className="microphone-result-container">
          <div className="microphone-result-text">{transcript}</div>
        </div>
      )}
      <div className="mircophone-container">
        <div
          className="microphone-icon-container"
          ref={microphoneRef}
          onClick={handleListing}
        >
          <img src={microPhoneIcon} className="microphone-icon" />
        </div>
        
        {/*<div className="microphone-status">
          {isListening ? "Habla ahora........." : "Click "}
        </div>*/
        }
        {isListening && (
          <>
          <button className="microphone-reset btn" onClick={()=>{
            handleReset()
            handleReset()
          }}>
            Borrar
          </button>
          <button className="microphone-stop btn" onClick={sendData}>
            Enviar
          </button>
          </>
        )}
      </div>
      
    </div>
  )
}

export default VoiceToText