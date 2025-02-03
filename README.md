<div align="center">
<h3 align="center">Secret Santa Bot</h3>

  <p align="center">
    A bot for facilitating Secret Santa gift exchanges within Discord servers.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#architecture">Architecture</a>
      <ul>
        <li><a href="#data">Data</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

### Key Features

- **Secret Santa Matching:** Randomly assigns participants as each other's Secret Santa, ensuring a fair and exciting gift exchange.
- **Direct Messaging:**  Privately informs each participant who their designated recipient is, maintaining the element of surprise.
- **Anonymous Requests:** Allows participants to discreetly request additional gift ideas or more specific details from their Secret Santa through the bot.
- **Administrative Controls:** Provides commands for administrators to start, manage, and end Secret Santa events within their Discord servers.

### Built With

- [Python](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)

<details>
<summary>Noteworthy Libraries Used</summary>

- [asyncio](https://docs.python.org/3/library/asyncio.html) - For asynchronous operations and managing timers.
- [csv](https://docs.python.org/3/library/csv.html) - For reading and writing data to CSV files.
- [json](https://docs.python.org/3/library/json.html) - For handling JSON data and configuration files.
- [os](https://docs.python.org/3/library/os.html) - For interacting with the operating system, such as creating directories.
- [random](https://docs.python.org/3/library/random.html) - For generating random numbers and selections.

</details>

## Architecture

![secret-santa-architecture](https://github.com/user-attachments/assets/bdcb4ce3-7f77-438b-a972-9cdaf0af7cfc)

### Data

The bot stores data in the following structures:

```ts
// global_participants.txt
{
  [participantId: string]: guildId: number;
}
```
```ts
// state_[guildId].txt
{
  started: boolean,
  names_drawn: boolean
}
```
```ts
// TOP_SECRET_[guildId].txt
{
  [santaId: string]: victimId: string;
}
```
```ts
// start_message_id_[guildId].json
{
  [channelName: string]: messageId: string;
}
```
```ts
// channel_name_[guildId].json
{
  [guildId: string]: channelName: string;
}
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- A Discord account and server
- A Discord bot application and token (refer to the Discord Developer Portal)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/username/repo.git
   ```
2. Navigate to the project directory:
   ```sh
   cd secret-santa
   ```
3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure the bot:
   - Create a file named `config.json` in the project directory.
   - Add your bot token to the `config.json` file:
     ```json
     {
       "token": "YOUR_BOT_TOKEN"
     }
     ```
5. Start the bot:
   ```sh
   python secret_santa.py
   ```

## Acknowledgments

- Generated with [HackMate](https://github.com/owengretzinger/hackmate) — an AI tool that understands your entire codebase.
