import React from 'react'
import "./chat.css"
const Chat = () => {
  return (
    <div>
        <div class="chat-container">
        <div class="message received">
            <div class="message-content">
                <p>Hello! How can I help you?</p>
            </div>
        </div>
        <div class="message sent">
            <div class="message-content">
                <p>Hi there! I have a question.</p>
            </div>
        </div>
        <div class="message sent">
            <div class="message-content">
                <p>Hi there! I have a question.</p>
            </div>
        </div>
        <div class="message received">
            <div class="message-content">
                <p>Hello! How can I help you?</p>
            </div>
        </div>
    </div>
    </div>
  )
}

export default Chat