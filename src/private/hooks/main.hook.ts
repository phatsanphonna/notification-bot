import { WebhookClient, MessageEmbed } from 'discord.js';
import 'dotenv/config';
import { data, user } from '../private.service';

export function sendHooksToMain(data: data, user: user) {
  try {
    const webhook = new WebhookClient({ url: process.env.WEBHOOK_URL });
    const embed = new MessageEmbed();

    embed.setTitle(`${user.username} add an notification`);
    embed.setDescription(`**Subject**: ${data.subject}
    **Note**: ${data.notes}`);
    embed.setColor('BLUE');
    embed.setAuthor(user.username, user.avatarurl);
    webhook.send({
      username: 'Alert Bot Hook',
      embeds: [embed],
      avatarURL: process.env.AVATAR,
    });
  } catch (err) {
    console.log(err);
  }
}
