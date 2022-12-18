import { formatDate } from '@angular/common';
import { Component, ViewChild} from '@angular/core';
import { faPaperPlane } from '@fortawesome/free-regular-svg-icons';

@Component({
  selector: 'chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.scss']
})



export class ChatWindowComponent {
  faArrowRight = faPaperPlane;
  data: string = '';

  writing: boolean = true
  startTime = formatDate(Date.now(),'HH:mm:ss', 'en-US'); 
  //startTime: string = new Date().toTimeString()
  messages: Array<Message> = [new Message("FRI", "Ahoj, ako ti môžem pomôcť?", "10:55"), new Message("student", "Kedy bude chatbot hotový?", "10:55"), new Message("FRI", "Dobrá otázka.", "10:58"), new Message("FRI", "Robíme všetko pre to, aby to bolo čo najskôr?", "10:58")]

  onMouseEnter() {
    console.log("jou")
  }

  addStudentMessage(text : string) {
    this.messages.push(new Message("student", this.data = text, new Date().toTimeString()))
    getAnswer(text)
  }
}

export class Message {
  author: string
  text: string
  time: string

  constructor(author:string, text:string, time:string) {
      this.author = author;
      this.text = text;
      this.time = time;
  }
}

async function getAnswer(sentence: string) {
  try {
    console.log(sentence)
    // 👇️ const response: Response
    const response = await fetch('http://localhost:8000/api/messages', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    const result = (await response.json()) as GetAnswerResponse;

    console.log('result is: ', JSON.stringify(result, null, 4));

    return result;
  } catch (error) {
    if (error instanceof Error) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

type GetAnswerResponse = {
  data: Message;
};
