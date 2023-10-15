import { useEffect, useRef, useState } from "react";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import microPhoneIcon from "../../assets/microphone.png";
import Chat from "../../components/chat/chat";
import vivianHablando from "../../assets/vivianHablando.png"
import VoiceToText from "../../components/voiceToText/voiceToText";
import Header from "../../assets/Header.png"
const url = "http://172.21.3.100:8000/"

const AgentPage = () => {
    const talktToVivi = async (mesage)=>{
        const res = await fetch(url)
        const vivisResponse = await res.json()
        handleTalk(vivisResponse.propouse)
      }
      const [escribiendo, setEscribiendo] = useState(false )
      const synth = window.speechSynthesis;
    
      const handleTalk = (speech) => {
        const msg = new SpeechSynthesisUtterance()
    
        msg.text = speech
        msg.volume = 10
        synth.speak(msg)
    
      }
      return (
        <div className="page" >
        <img src={Header}/>
        <img src={vivianHablando}  />
         {escribiendo ? <p className="escuchando">Escucando...</p>:null}
          <Chat />
          <VoiceToText setEscribiendo = {setEscribiendo} talktToVivi={(mesage) => talktToVivi(mesage)}/>
        </div>
      );
}

export default AgentPage