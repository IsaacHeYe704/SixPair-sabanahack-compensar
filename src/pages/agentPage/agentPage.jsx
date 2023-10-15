import { useEffect, useRef, useState } from "react";
import microPhoneIcon from "../../assets/microphone.png";
import Chat from "../../components/chat/chat";
import vivianHablando from "../../assets/vivianHablando.png"
import VoiceToText from "../../components/voiceToText/voiceToText";
import Header from "../../assets/Header.png"
const url = "http://172.21.3.100:8000/predict"

const AgentPage = () => {
    const [loading, setloading] = useState(false)
    const talktToVivi = async (mesage)=>{
        let aux = [{
            type: "send",
            text: mesage
        },...history]
        sethistory(aux)
        let data = {
            "text":mesage
        }
        setloading(true)
        const res = await fetch(url, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            body: JSON.stringify(data),
        })
        const vivisResponse = await res.json()
        let auxtwo = [{
            type: "received",
            text: vivisResponse.activity
        },...aux]
        setloading(false)
        sethistory(auxtwo)
        handleTalk(vivisResponse.activity)
      }
      const [escribiendo, setEscribiendo] = useState(false )
      const synth = window.speechSynthesis;
    
      const handleTalk = (speech) => {
        const msg = new SpeechSynthesisUtterance()
    
        msg.text = speech
        msg.volume = 10
        synth.speak(msg)
        let r = setInterval(() => {
            console.log(synth.speaking);
            if (!synth.speaking) {
              clearInterval(r);
            } else {
                synth.resume();
            }
          }, 1000);
    
      }
      const [history, sethistory] = useState([])
      
      return (
        <div className="page" >
        <img src={Header}/>
        <img className="vivian" src={vivianHablando}  />
        
         {escribiendo ? <p className="escuchando">Escucando...</p>:null}
          <Chat history={history.reverse()} />
          {loading ? <span class="loader"></span> : null}http://localhost:5173/
          http://localhost:5173/
          <VoiceToText setEscribiendo = {setEscribiendo} talktToVivi={(mesage) => talktToVivi(mesage)}/>
        </div>
      );
}

export default AgentPage