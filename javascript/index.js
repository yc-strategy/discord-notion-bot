require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// 当 bot 准备好时
client.once('ready', () => {
    console.log(`Bot已登录为 ${client.user.tag}`);
});

// 当收到消息时
client.on('messageCreate', async message => {
    // 忽略机器人自己的消息
    if (message.author.bot) return;

    // 测试命令：当用户发送 !ping 时
    if (message.content === '!ping') {
        await message.reply('Pong!');
    }
});

// 使用 token 登录 Discord
client.login(process.env.DISCORD_TOKEN);