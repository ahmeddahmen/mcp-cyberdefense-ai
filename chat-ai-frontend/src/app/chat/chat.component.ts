import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { marked } from 'marked';
import { ChatMessage, ChatService } from '../services/chat.service';

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule, DatePipe],
  templateUrl: './chat.component.html',
  standalone: true,
  styleUrl: './chat.component.css'
})
export class ChatComponent implements AfterViewChecked {
  @ViewChild('chatContainer') private chatContainer!: ElementRef;

  messages: ChatMessage[] = [];
  newMessage: string = '';
  isLoading: boolean = false;
  isTyping: boolean = false;

  constructor(private chatService: ChatService) {
    this.messages.push({
      content: `👋 Bonjour ! Je suis votre **agent IA de cyberdéfense**.

Je peux vous aider à :
- 🔍 **Analyser les logs SSH** et détecter les attaques par force brute
- 🌐 **Scanner les ports** d'un hôte cible
- 🔗 **Surveiller les connexions réseau** suspectes
- 📊 **Générer des rapports de sécurité**

Utilisez les boutons rapides ci-dessus ou posez-moi une question en langage naturel.`,
      isUser: false,
      timestamp: new Date()
    });
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  private scrollToBottom(): void {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }

  sendQuick(message: string): void {
    this.newMessage = message;
    this.sendMessage();
  }

  sendMessage(): void {
    if (!this.newMessage.trim() || this.isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      content: this.newMessage,
      isUser: true,
      timestamp: new Date()
    };

    this.messages.push(userMessage);
    const messageToSend = this.newMessage;
    this.newMessage = '';
    this.isLoading = true;
    this.isTyping = true;

    this.chatService.sendMessage(messageToSend).subscribe({
      next: (response: any) => {
        this.isTyping = false;
        const aiMessage: ChatMessage = {
          content: response,
          isUser: false,
          timestamp: new Date()
        };
        this.messages.push(aiMessage);
        this.isLoading = false;
      },
      error: (error: any) => {
        this.isTyping = false;
        console.error('Error:', error);
        const errorMessage: ChatMessage = {
          content: '⚠️ Une erreur s\'est produite lors du traitement de votre requête. Veuillez réessayer.',
          isUser: false,
          timestamp: new Date()
        };
        this.messages.push(errorMessage);
        this.isLoading = false;
      }
    });
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  parseMarkdown(content: string): string {
    return marked.parse(content) as string;
  }
}
