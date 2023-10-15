import React, { useEffect, useState } from 'react'
import "./chat.css"
const Chat = ({history}) => {
 useEffect(() => {
    console.log("logeando");
   console.log(history);
 }, [])

  return (
    <div>
        <div class="chat-container">
   {
    history.map((message) =>(
        message.type === "send" ? 
        <div className="message sent">
            <div class="message-content">
                <p>{message.text}</p>
            </div>
        </div>:
        <div className="message received">
            <div class="message-content">
                <p>{message.text}</p>
            </div>
        </div>
    ))
   }
        

        
    </div>
    </div>
  )
}

export default Chat