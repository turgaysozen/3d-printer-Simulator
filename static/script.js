// const socket = io('http://localhost:8080');

// socket.on('printer_data', (data) => {
//     const printerDataElement = document.getElementById('printerData');
//     const temperatureFill = document.getElementById('temperatureFill');
//     const fanSpeedFill = document.getElementById('fanSpeedFill');
//     const printProgressFill = document.getElementById('printProgressFill');
//     const filamentUsageFill = document.getElementById('filamentUsageFill');
//     const leftFilamentFill = document.getElementById('leftFilamentFill');

//     const { temperature, fan_speed, print_progress, filament_usage, left_filament } = JSON.parse(data);

//     printerDataElement.innerText = data;

//     // Update fill percentages
//     updateFillPercentage(temperatureFill, temperature);
//     updateFillPercentage(fanSpeedFill, fan_speed);
//     updateFillPercentage(printProgressFill, print_progress);
//     updateFillPercentage(filamentUsageFill, filament_usage);
//     updateFillPercentage(leftFilamentFill, left_filament);
// });

// function updateFillPercentage(element, value) {
//     const fillPercentage = (value / maxValue) * 100; // Adjust maxValue based on the range of values
//     element.style.clip = `rect(0, 50px, 100px, ${50 - (50 * fillPercentage) / 100}px)`;
// }

// function sendControlCommand(command) {
//     socket.emit('control_printer', { command });
// }
