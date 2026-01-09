# Highrise Blackjack Casino Bot

## Overview
A professional English-language Blackjack casino bot for Highrise with real gold payment integration, multiple casino games, admin system, and many advanced features.

## Features
- **Real Gold Payment System**: Users tip the bot gold to add credits, then play with !play command
- **Multiple Casino Games**: Blackjack, Slots, Dice, Coinflip, Roulette
- **Jackpot System**: 5% of bets go to jackpot, win by hitting 777 in slots
- **Daily Rewards**: Daily login bonus with streak system
- **VIP System**: VIP users get bonus daily rewards
- **Admin System**: Full admin/owner hierarchy with moderation commands
- **Equip System**: Copy any user's outfit with `equip @username`
- **Emote System**: 50+ emotes with loop functionality
- **Teleport System**: Save and teleport to locations
- **Statistics**: Track player wins, losses, wagered amounts
- **Custom Commands**: Create custom chat responses

## Game Commands
| Command | Description |
|---------|-------------|
| `!play [amount]` | Play blackjack with gold credits (max 10000g) |
| `!bet [amount]` | Play blackjack with virtual coins |
| `!slots [amount]` | Slot machine game |
| `!dice [high/low] [amount]` | Dice game |
| `!coinflip [heads/tails] [amount]` | Coin flip game |
| `!roulette [red/black/green/num] [amount]` | Roulette game |
| `!hit` | Draw another card |
| `!stand` | Stand with current hand |
| `!double` | Double down (first 2 cards only) |

## Account Commands
| Command | Description |
|---------|-------------|
| `!credits` | Check gold credit balance (whisper) |
| `!bal` | Check virtual coin balance (whisper) |
| `!deposit` | Instructions to add gold credits |
| `!withdraw [amount]` | Withdraw gold to your account |
| `!daily` | Claim daily reward |
| `!stats` | View your statistics |
| `!top [credits/wins/wagered]` | View leaderboard |
| `!gift [name] [amount]` | Gift credits to another player |
| `!jackpot` | View jackpot info |

## Social Commands
| Command | Description |
|---------|-------------|
| `equip @username` | Copy user's outfit to bot |
| `!emote [name]` | Perform an emote |
| `!emotes` | List all available emotes |
| `!loop [emote]` | Loop an emote continuously |
| `!stoploop` | Stop emote loop |
| `!react [type] [@user]` | Send reaction |

## Admin Commands
| Command | Description |
|---------|-------------|
| `!kick [user]` | Kick user from room |
| `!mute [user] [mins]` | Mute user |
| `!unmute [user]` | Unmute user |
| `!bring [user]` | Teleport user to you |
| `!goto [user]` | Teleport to user |
| `!tp [location/x y z]` | Teleport to location |
| `!savetp [name]` | Save teleport location |
| `!follow [user]` | Follow user |
| `!unfollow` | Stop following |
| `!say [text]` | Make bot say message |
| `!whisper [user] [msg]` | Send whisper |
| `!addcmd [trigger] [response]` | Add custom command |
| `!removecmd [trigger]` | Remove custom command |
| `!addvip [user]` | Add VIP user |
| `!removevip [user]` | Remove VIP user |

## Owner Commands
| Command | Description |
|---------|-------------|
| `!ban [user]` | Ban user |
| `!unban [user]` | Unban user |
| `!addadmin [user]` | Add admin |
| `!removeadmin [user]` | Remove admin |
| `!addowner [user]` | Add owner |
| `!removeowner [user]` | Remove owner |
| `!setcredits [user] [amount]` | Set user credits |
| `!addcredits [user] [amount]` | Add credits to user |
| `!tip [user] [amount]` | Tip user gold |
| `!tipall [amount]` | Tip all users |
| `!wallet` | Check bot wallet |

## Data Files
- `credits.json` - Gold credit balances
- `balances.json` - Virtual coin balances
- `user_stats.json` - Player statistics
- `jackpot.json` - Jackpot data
- `daily_rewards.json` - Daily reward claims
- `admins.json` - Admin list
- `owners.json` - Owner list
- `vip_users.json` - VIP user list
- `banned_users.json` - Banned users
- `muted_users.json` - Muted users
- `teleport_positions.json` - Saved teleport locations
- `custom_commands.json` - Custom chat commands
- `user_cache.json` - Username to ID cache

## Environment Variables
- `HIGHRISE_ROOM_ID` - Room ID for the bot
- `HIGHRISE_BOT_TOKEN` - Bot API token (store as secret)

## Recent Changes
- December 2025: Updated welcome system - whisper with commands list on join
- December 2024: Converted to English language
- December 2024: Added real gold tip-to-play system (max 10000g)
- December 2024: Added equip system
- December 2024: Removed public welcome messages (whisper only for !help)
- December 2024: Added Slots, Dice, Coinflip, Roulette games
- December 2024: Added Jackpot system
- December 2024: Added Daily rewards with streak
- December 2024: Added Admin/Owner/VIP system
- December 2024: Added Emote system with 50+ emotes
- December 2024: Added Statistics tracking
- December 2024: Added Teleport system
- December 2024: Added Custom commands

## Welcome System
When a user joins the room, they receive a whisper (private message) with all the main bot commands. This keeps the welcome message small and private, not visible to others in chat.
