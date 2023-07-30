const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const readline = require('readline');
const fs = require('fs')
const axios = require('axios');
const client = new Client({ authStrategy: new LocalAuth() });
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
});

// Function to send a message to a number
async function sendMessageToNumber(number, message) {
    const chat = await client.getChatById(number);
    if (chat) {
        chat.sendMessage(message);
        console.log(`Message sent to ${number}`);
    } else {
        console.log(`No chat found for ${number}`);
    }
}

// Event when the client is ready
client.on('ready', () => {
    console.log('Client is ready!');
});

// Event when the client is disconnected
client.on('disconnected', (reason) => {
    console.log(`Client disconnected: ${reason}`);
});

let adminloggedinusers = [];
const userInteractions = {};
let abc=  new FormData();
client.on('message', async (message) => {
    const userFrom = message.from;
    if (adminloggedinusers.includes(userFrom)) {
        try {
           
            let criminal = {};
            if (message.hasMedia && message.type === 'image') {

                const mediaData = await message.downloadMedia();
                const fileName = `DI_${Date.now()}.${mediaData.mimetype.split('/')[1]}`;
                fs.writeFileSync(fileName, mediaData.data, 'base64');
                const formData = new FormData();
                console.log(`Image saved: ${fileName}`);

                formData.append('fileName', fileName);
                abc.append('fileName',fileName);
                const res = await axios.post('http://127.0.0.1:5000/dbwrite', formData)
                if (res.data.name)
                    message.reply((`Name : ${res.data.name} \nCrime: ${res.data.crime} \nAdditional Information: ${res.data.additionalInfo}`));
                else
                    message.reply((res.data))

                if (res.data == 'success') {
                    if (!userInteractions[userFrom]) {
                        userInteractions[userFrom] = {};
                        message.reply("enter name") // Create an empty interaction object for the user
                        userInteractions[userFrom].name = true;
                        console.log(formData);
                    }
                }
            }

            else {
                
                if (userInteractions[userFrom].name && !userInteractions[userFrom].crime) {
                    // User should enter name
                    const name = message.body.trim();
                    if (name !== 'exit') {
                        abc.append('name', message.body)
                        userInteractions[userFrom].crime = true;
                        client.sendMessage(userFrom, 'Enter crime')
                    }
                    else{
                     delete userInteractions[userFrom];
                     abc = new FormData();
                    }
                } else if (userInteractions[userFrom].name && userInteractions[userFrom].crime && !userInteractions[userFrom].additionalInfo) {
                    // User should enter crime
                    const crime = message.body.trim();
                    if (crime !== 'exit') {
                        criminal.crime = message.body;
                        userInteractions[userFrom].additionalInfo = true;
                        abc.append('crime', message.body)
                        client.sendMessage(userFrom, 'Enter additional info')
                    }
                    else{
                      delete userInteractions[userFrom];
                      abc = new FormData();
                    }
                } else if (userInteractions[userFrom].name && userInteractions[userFrom].crime && userInteractions[userFrom].additionalInfo) {
                    // User should enter additional info
                    const additionalInfo = message.body.trim();
                    if (additionalInfo !== 'exit') {
                        userInteractions[userFrom].additionalInfo = additionalInfo;
                        criminal.additionalInfo = message.body;
                        abc.append('additionalInfo', message.body)
                        const sentCriminal = await axios.post('http://127.0.0.1:5000/store', abc);
                        message.reply((sentCriminal.data));
                        client.sendMessage(userFrom, 'done')
                        abc = new FormData();
                        delete userInteractions[userFrom];
                    }
                    else {
                     delete userInteractions[userFrom];
                     abc = new FormData();
                    }
                }
            }
        } catch (error) {
            console.error('Error occurred while downloading the image:', error);
        }
    }
});
// client.on('message', (msg) => {
//   if (msg.body === 'dbadmin') {
//     // Start the conversation by prompting the user to enter a number and a message
//     client.sendMessage(msg.from, 'Enter the id').then(() => {
//       client.once('message', (idMsg) => {
//         if (idMsg.body == 'shubhambetu')
//           client.sendMessage(msg.from, 'Enter password').then(() => {
//             console.log('test')
//             const checkPassworda = (passwordMsg) => {
//               if (passwordMsg.body == 'shubham@12')

//                 client.sendMessage(msg.from, 'Verification successful').then(() => {
//                   console.log('1')
//                   if (!adminloggedinusers.includes(msg.from)){
//                     adminloggedinusers.push(msg.from)
//                     console.log(adminloggedinusers)
//                   }
//                 })

//               else
//                 passwordMsg.reply("invalid password").then(() => {
//                    client.once('message', checkPassworda);
//                   console.log('2')
//                 });

//             };
//           });
//       });
//     });
//   }
// });
client.on('message', (msg) => {
    if (msg.body === 'dbadmin') {
        // Start the conversation by prompting the user to enter a number and a message
        client.sendMessage(msg.from, 'Enter the id').then(() => {
            client.once('message', (idMsg) => {
                if (idMsg.body == 'shubhambetu')
                    client.sendMessage(msg.from, 'Enter password').then(() => {
                        // Initialize a variable to keep track of the number of password attempts
                        // Define a function to check the password
                        const checkPassword = (passwordMsg) => {
                            // Increment the number of password attempts
                            if (passwordMsg.body == 'shubham@12')
                                client.sendMessage(msg.from, 'Verification successful').then(() => {
                                    // Push the user's chat id to the array of logged in users

                                    if (!adminloggedinusers.includes(msg.from)) {
                                        adminloggedinusers.push(msg.from);
                                        console.log(adminloggedinusers)
                                    }
                                })
                            else
                                // Check if the number of password attempts has reached the limit
                                // Prompt the user to enter the password again
                                passwordMsg.reply("Invalid Password. Please try again.").then(() => {
                                    // Listen for the next message from the user
                                    client.once('message', checkPassword);
                                });

                        };
                        // Listen for the first message from the user
                        client.once('message', checkPassword);
                    });
            });
        });
    }
});

let loggedInUsers = [];
client.on('message', async (message) => {
    if (loggedInUsers.includes(message.from)) {
        try {
            if (message.hasMedia && message.type === 'image') {
                // Check if the user's chat id is in the arrày of logged in users
                if (loggedInUsers.includes(message.from)) {
                    console.log(loggedInUsers)
                    const mediaData = await message.downloadMedia();
                    const fileName = `DI_${Date.now()}.${mediaData.mimetype.split('/')[1]}`;
                    fs.writeFileSync(fileName, mediaData.data, 'base64');

                    const formData = new FormData();
                    formData.append('file', fileName);
                    const res = await axios.post('http://127.0.0.1:5000/dbsearch', formData)
                    if (res.data.name)
                        message.reply((`Name : ${res.data.name} \nCrime: ${res.data.crime} \nAdditional Information: ${res.data.additionalInfo}`));
                    else
                        message.reply(res.data)
                    console.log(res.data);
                }
            }
        } catch (error) {
            console.error('Error occurred while downloading the image:', error);
        }
    }
});
client.on('message', (msg) => {
    if (msg.body === 'dbsearch') {
        // Start the conversation by prompting the user to enter a number and a message
        client.sendMessage(msg.from, 'Enter the id').then(() => {
            client.once('message', (idMsg) => {
                if (idMsg.body == 'DURG007')
                    client.sendMessage(msg.from, 'Enter password').then(() => {
                        // Initialize a variable to keep track of the number of password attempts
                        // Define a function to check the password
                        const checkPassword = (passwordMsg) => {
                            // Increment the number of password attempts
                            if (passwordMsg.body == 'DURG@12')
                                client.sendMessage(msg.from, 'Verification successful').then(() => {
                                    // Push the user's chat id to the array of logged in users

                                    if (!loggedInUsers.includes(msg.from)) {
                                        loggedInUsers.push(msg.from);
                                        console.log(loggedInUsers)
                                    }
                                })
                            else
                                // Check if the number of password attempts has reached the limit
                                // Prompt the user to enter the password again
                                passwordMsg.reply("Invalid Password. Please try again.").then(() => {
                                    // Listen for the next message from the user
                                    client.once('message', checkPassword);
                                });

                        };
                        // Listen for the first message from the user
                        client.once('message', checkPassword);
                    });
            });
        });
    }
});

// Start the client
client.initialize();
