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

client.on('message', (msg) => {
  if (msg.body === 'dbadmin') {
    // Start the conversation by prompting the user to enter a number and a message
    client.sendMessage(msg.from, 'Enter the id').then(() => {
      client.once('message', (idMsg) => {
        if (idMsg.body == 'shubhambetu')
          client.sendMessage(msg.from, 'Enter password').then(() => {
            client.once('message', (passwordMsg) => {
              if (passwordMsg.body == 'shubham@12')
                client.sendMessage(msg.from, 'Verification successful').then(() => {
                  client.on('message', async (message) => {
                    try {
                      if (message.hasMedia && message.type === 'image') {
                        const mediaData = await message.downloadMedia();
                        const fileName = `DI_${Date.now()}.${mediaData.mimetype.split('/')[1]}`;
                        fs.writeFileSync(fileName, mediaData.data, 'base64');

                        console.log(`Image saved: ${fileName}`);

                        const formData = new FormData();
                        formData.append('fileName', fileName);

                        const res = await axios.post('http://localhost:8000/dbwrite', formData)
                        if (res.data.name)
                          message.reply((`Name : ${res.data.name} \nCrime: ${res.data.crime} \nAdditional Information: ${res.data.additionalInfo}`));
                        else
                          message.reply((res.data))
                        let criminal = {};
                        if (res.data == 'success') {
                          message.reply("Enter name").then(() => {
                            client.once('message', (namemsg) => {
                              formData.append('name', namemsg.body)
                              client.sendMessage(message.from, 'Enter crime').then(() => {
                                client.once('message', (crimemsg) => {
                                  criminal.crime = crimemsg.body;
                                  formData.append('crime', crimemsg.body)
                                  client.sendMessage(message.from, 'Enter additional info').then(() => {
                                    client.once('message', async (addinfomsg) => {
                                      criminal.additionalInfo = addinfomsg.body;
                                      formData.append('additionalInfo', addinfomsg.body)
                                      const sentCriminal = await axios.post('http://localhost:8000/store', formData);
                                      addinfomsg.reply((sentCriminal.data));
                                    })
                                  })
                                });
                              })
                            })
                          })
                        }
                        console.log(res.data);
                      }
                    } catch (error) {
                      console.error('Error occurred while downloading the image:', error);
                    }
                  });
                })
              else
                passwordMsg.reply("invalid password")
            });
          });
      });
    });
  }
});
// client.on('message', (msg) => {

//   if (msg.body === 'dbsearch') {
//     // Start the conversation by prompting the user to enter a number and a message
//     client.sendMessage(msg.from, 'Enter the id').then(() => {
//       client.once('message', (idMsg) => {
//         if (idMsg.body == 'DURG007')
//           client.sendMessage(msg.from, 'Enter password').then(() => {
//             client.once('message', (passwordMsg) => {
//               if (passwordMsg.body == 'DURG@12')
//                 client.sendMessage(msg.from, 'Verification successful').then(() => {
//                   client.on('message', async (message) => {
//                     try {
//                       if (message.hasMedia && message.type === 'image') {
//                         const mediaData = await message.downloadMedia();
//                         const fileName = `DI_${Date.now()}.${mediaData.mimetype.split('/')[1]}`;
//                         fs.writeFileSync(fileName, mediaData.data, 'base64');

//                         console.log(`Image saved: ${fileName}`);

//                         const formData = new FormData();
//                         formData.append('fileName', fileName);

//                         const res = await axios.post('http://localhost:8000/process_image', formData)
//                         if (res.data.name)
//                           message.reply((`Name : ${res.data.name} \nCrime: ${res.data.crime} \nAdditional Information: ${res.data.additionalInfo}`));
//                         else
//                           message.reply("THIS person is not black")  
//                         console.log(res.data);
//                       }
//                     } catch (error) {
//                       console.error('Error occurred while downloading the image:', error);
//                     }
//                   });
//                 })
//               else
//                  passwordMsg.reply("Invalid Password").then
//             });
//           });
//       });
//     });
//   }
// });

// client.on('message', (msg) => {
//   if (msg.body === 'dbsearch') {
//     // Start the conversation by prompting the user to enter a number and a message
//     client.sendMessage(msg.from, 'Enter the id').then(() => {
//       client.once('message', (idMsg) => {
//         if (idMsg.body == 'DURG007')
//           client.sendMessage(msg.from, 'Enter password').then(() => {
//             // Initialize a variable to keep track of the number of password attempts
//             let passwordAttempts = 0;
//             // Define a function to check the password
//             const checkPassword = (passwordMsg) => {
//               // Increment the number of password attempts
//               passwordAttempts++;
//               if (passwordMsg.body == 'DURG@12')
//                 client.sendMessage(msg.from, 'Verification successful').then(() => {

//                   client.on('message', async (message) => {
//                     try {
//                       if (message.hasMedia && message.type === 'image') {
//                         const mediaData = await message.downloadMedia();
//                         const fileName = `DI_${Date.now()}.${mediaData.mimetype.split('/')[1]}`;
//                         fs.writeFileSync(fileName, mediaData.data, 'base64');

//                         console.log(`Image saved: ${fileName}`);

//                         const formData = new FormData();
//                         formData.append('fileName', fileName);

//                         const res = await axios.post('http://localhost:8000/process_image', formData)
//                         if (res.data.name)
//                           message.reply((`Name : ${res.data.name} \nCrime: ${res.data.crime} \nAdditional Information: ${res.data.additionalInfo}`));
//                         else
//                           message.reply("THIS person is not black")  
//                         console.log(res.data);
//                       }
//                     } catch (error) {
//                       console.error('Error occurred while downloading the image:', error);
//                     }
//                   });
//                 })
//               else
//                 // Check if the number of password attempts has reached the limit
//                   // Prompt the user to enter the password again
//                   passwordMsg.reply("Invalid Password. Please try again.").then(() => {
//                     // Listen for the next message from the user
//                     client.once('message', checkPassword);
//                   });

//             };
//             // Listen for the first message from the user
//             client.once('message', checkPassword);
//           });
//       });
//     });
//   }
// });
let loggedInUsers = [];
client.on('message', (msg) => {
  if (msg.body === 'dbsearch') {
    // Start the conversation by prompting the user to enter a number and a message
    client.sendMessage(msg.from, 'Enter the id').then(() => {
      client.once('message', (idMsg) => {
        if (idMsg.body == 'DURG007')
          client.sendMessage(msg.from, 'Enter password').then(() => {
            // Initialize a variable to keep track of the number of password attempts
            let passwordAttempts = 0;
            // Define a function to check the password
            const checkPassword = (passwordMsg) => {
              // Increment the number of password attempts
              passwordAttempts++;
              if (passwordMsg.body == 'DURG@12')
                client.sendMessage(msg.from, 'Verification successful').then(() => {
                  // Push the user's chat id to the array of logged in users
                  if (!loggedInUsers.includes(msg.from)){
                    loggedInUsers.push(msg.from);
                    console.log(loggedInUsers)
                  }

                  client.on('message', async (message) => {
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
                          const res = await axios.post('http://localhost:8000/dbsearch', formData)
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
                  });
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
