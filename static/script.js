const socket = io('http://localhost:5000', { reconnection: true });

socket.on('connect', () => {
    console.log('Connected from the server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from the server');
});

socket.on('printer_data', (data) => {
    const printerDataElement = document.getElementById('printerData');
    const temperatureFill = document.getElementById('temperatureFill');
    const fanSpeedFill = document.getElementById('fanSpeedFill');
    const printProgressFill = document.getElementById('printProgressFill');
    const filamentUsageFill = document.getElementById('filamentUsageFill');
    const leftFilamentFill = document.getElementById('leftFilamentFill');
    const temperatureValue = document.getElementById('temperatureValue');
    const fanSpeedValue = document.getElementById('fanSpeedValue');
    const printProgressValue = document.getElementById('printProgressValue');
    const leftFilamentValue = document.getElementById('leftFilamentValue');

    const { temperature, fan_speed, print_progress, filament_usage, left_filament, printer_name, status, print_time } = JSON.parse(data);

    if (status === 'Idle') {
        printerDataElement.innerText = 'Printer is Idle'
        pauseButton.style.opacity = '0.5';
        continueButton.style.opacity = '0.5';
        stopButton.style.opacity = '0.5';

        pauseButton.style.pointerEvents = 'none';
        continueButton.style.pointerEvents = 'none';
        stopButton.style.pointerEvents = 'none';

        printerDataElement.innerHTML = `<strong>Printer Name:</strong> ${printer_name}<br><strong>Status:</strong> ${status}<br><strong>Filament Usage:</strong> 0g / 1000g<br><strong>Printing Time:</strong> 0`;
        return
    }

    updateButtonStates(status);

    printerDataElement.innerHTML = `<strong>Printer Name:</strong> ${printer_name}<br><strong>Status:</strong> ${status}<br><strong>Filament Usage:</strong> ${filament_usage}g / 1000g<br><strong>Printing Time:</strong> ${print_time}`;

    updateFillPercentage(temperatureFill, temperature, 100);
    updateFillPercentage(fanSpeedFill, fan_speed, 100);
    updateFillPercentage(printProgressFill, print_progress, 100);
    updateFillPercentage(leftFilamentFill, left_filament, 100);

    temperatureValue.innerText = `${temperature.toFixed(2)} °C`;
    fanSpeedValue.innerText = `${fan_speed.toFixed(2)} %`;
    printProgressValue.innerText = `${print_progress.toFixed(2)} %`;
    leftFilamentValue.innerText = `${left_filament.toFixed(2)} %`;

    if (print_progress >= 100 && status !== 'Completed') {
        sendControlCommand('finish');
        document.getElementById('printerData').style.backgroundColor = '#A8E4A0';
        printerDataElement.innerHTML = `<strong>Printer Name:</strong> ${printer_name}<br><strong>Status:</strong> Done!<br><strong>Filament Usage:</strong> ${filament_usage}g / 1000g<br><strong>Printing Time:</strong> ${print_time}`;
    }
});

function updateFillPercentage(element, value, maxValue) {
    const fillPercentage = (value / maxValue) * 100;
    element.style.width = `${fillPercentage}%`;
}

function sendControlCommand(command) {
    socket.emit('control_printer', { command });
}

function increaseTimerSpeed() {
    socket.emit('increase_timer_speed', { factor: 10 });
}

const controls = document.getElementsByClassName('control-button');

const pauseButton = controls[0];
const continueButton = controls[1];
const stopButton = controls[2];
const startButton = controls[3];

function updateButtonStates(status) {
    pauseButton.style.opacity = '1';
    continueButton.style.opacity = '1';
    stopButton.style.opacity = '1';
    startButton.style.opacity = '1';

    pauseButton.style.pointerEvents = 'auto';
    continueButton.style.pointerEvents = 'auto';
    stopButton.style.pointerEvents = 'auto';
    startButton.style.pointerEvents = 'auto';

    const printerDataElement = document.getElementById('printerData');

    if (status === 'Paused') {
        continueButton.style.opacity = '1';
        pauseButton.style.opacity = '0.5';
        startButton.style.opacity = '0.5';
        stopButton.style.opacity = '0.5';

        pauseButton.style.pointerEvents = 'none';
        startButton.style.pointerEvents = 'none';
        stopButton.style.pointerEvents = 'none';

        printerDataElement.style.backgroundColor = '#FFA500';
    } else if (status === 'Printing') {
        startButton.style.opacity = '0.5';
        continueButton.style.opacity = '0.5';

        startButton.style.pointerEvents = 'none';
        continueButton.style.pointerEvents = 'none';

        printerDataElement.style.backgroundColor = '#89CFF0';
    } else if (status === 'Stopped') {
        startButton.style.opacity = '1';
        startButton.innerText = 'Print';
        pauseButton.style.opacity = '0.5';
        continueButton.style.opacity = '0.5';
        stopButton.style.opacity = '0.5';

        pauseButton.style.pointerEvents = 'none';
        continueButton.style.pointerEvents = 'none';
        stopButton.style.pointerEvents = 'none';

        printerDataElement.style.backgroundColor = '#FF3800';
    } else if (status === 'Completed') {
        pauseButton.style.opacity = '0.5';
        continueButton.style.opacity = '0.5';
        stopButton.style.opacity = '0.5';

        pauseButton.style.pointerEvents = 'none';
        continueButton.style.pointerEvents = 'none';
        stopButton.style.pointerEvents = 'none';
    }
}