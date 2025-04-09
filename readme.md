# 📚 WP Make.com Automations

A complete automation to:
- 📥 Fetch articles from **WordPress**
- 📤 Save them into a **Notion** database
- 🧠 Clean up the text and generate a **voiceover** using **Google Cloud TTS**
- 🪝 Manage files larger or smaller than 5000 bytes with two logic paths
- ☁️ Upload audio to **GCP Cloud Storage**
- 🔁 Update the original WordPress post with the audio player

---

## 🧱 Requirements

- Accounts on **WordPress**, **Notion**, **Make.com**, **Google Cloud Platform**
- WordPress **Make.com** plugin
- Enabled APIs in GCP:
  - Cloud Storage
  - Text-to-Speech
  - Cloud Run
  - Cloud Build

---

## ⚙️ Make.com Setup: Scenarios

This automation is divided into two main workflows:

- **Scenario 1** – WordPress → Notion
- **Scenario 2** – WordPress → Google Cloud TTS (VoiceOver)

---

# ✏️ Scenario 1/2: WordPress → Notion

### 📌 Goal

Automatically save each new WordPress post into a Notion database, preserving title, link, author, date, and formatted content.

### 🪜 Step-by-Step

1. **Connect WordPress to Make.com**
   - Install the Make plugin on WordPress
   - Copy the API key and paste it into Make.com

2. **Connect Notion to Make.com**
   - Create an integration in Notion (Internal Integration)
   - Give it access to the database
   - Create a database with these columns: `Title`, `Author`, `Date`, `Link`, `Number`

3. **Create the Make Scenario**
   - Module: `WordPress - Watch Posts`
     - Type: post
     - Status: all
     - Limit: 150

4. **Router**
   - Splits the flow between Notion and VoiceOver

5. **Module: Notion - Create a Page**
   - Adds the post data to Notion DB

6. **Module: Notion - Append Page Content**
   - Adds cleaned post content to the Notion page

---

# 🎙️ Scenario 2/2: WordPress → VoiceOver (GCP)

### 📌 Goal

Take a post, clean the text, convert it to audio using Google Cloud TTS, and update the WordPress post with the audio player.

---

## 🔁 Full Workflow

1. **WordPress – Watch Post**  
   Monitors newly published articles.

2. **Router – Flow Split**  
   Separates Notion logic from VoiceOver logic.

3. **Text Parser – Clean HTML**  
   Combines:
   ```
   {{1.title}} {{1.content}} {{1.date}}
   ```

4. **OpenAI – Advanced Text Cleanup**
   - Removes HTML, links, code, special characters
   - Keeps punctuation and structure intact

5. **Google Cloud Storage – Upload .txt**
   - Bucket: `wp-voiceovers`
   - Filename: `{{1.id}}.txt`
   - Content: `{{47.result}}` (OpenAI output)

6. **Custom JS – Check file size (5000 bytes)**
   ```python
   byteLength = input.encode('utf-8').__len__()
   return { "exceeds": byteLength > 5000 }
   ```

7. **Router – Based on file size**
   - ≤ 5000 bytes → Short flow (direct TTS)
   - > 5000 bytes → Long flow (Cloud Run API)

---

## 🔽 Flow A – File ≤ 5000 bytes

8. **Google Cloud Text-to-Speech**
   - Voice: `it-IT-Chirp-HD-F`
   - Output: `.mp3`

9. **Google Drive – Upload file**

10. **HTTP – Get public file link**

11. **GCP Cloud Storage – Final upload**

12. **WordPress – Update Post**
   - Embeds audio player for `.mp3`:
     ```html
     <audio controls>
       <source src="https://storage.googleapis.com/wp-voiceovers/{{1.id}}.mp3" type="audio/mpeg">
     </audio>
     ```

13. **Email – Send notification**

---

## 🔼 Flow B – File > 5000 bytes

8. **Text Parser – Extra cleanup**
   - Removes `\n`, newline characters, and invisible symbols

9. **HTTP – Call Cloud Run API**
   ```json
   {
     "text": "{{61.text}}",
     "language": "it-IT",
     "voice": "it-IT-Wavenet-B",
     "filename": "{{1.id}}.wav"
   }
   ```

10. **WordPress – Update Post**
    - Embeds audio player for `.wav`:
      ```html
      <audio controls>
        <source src="https://storage.googleapis.com/wp-voiceovers/{{1.id}}.wav" type="audio/mpeg">
      </audio>
      ```

11. **Email – Send notification**

---

## ✅ Result

- Posts are backed up in Notion
- Texts are cleaned with AI
- Audio voiceovers are auto-generated and uploaded to Cloud Storage
- WordPress posts are updated with audio players
- Notification email is sent after each run

---

## 🧠 Tips

- `blueprint.json` contains the full exported Make.com scenario
- You can customize voices in GCP Text-to-Speech
- Ideal for blog, news, or voice publishing automation

---

**Author:** Paolo Ronco  
**Email:** info@paoloronco.it
**Project:** Make.com + WordPress + GCP TTS VoiceOver + Notion DB