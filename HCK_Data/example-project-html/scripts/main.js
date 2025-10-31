//
// main.js - Skrypt zarządzający stanem i czasem rzeczywistym
//
document.addEventListener('DOMContentLoaded', () => {
    // 
    // SPRAWDZENIE CZASU STARTU 
    // Czas startu jest ustawiony w skrypcie inline w index.html dla najwyższej precyzji.
    const pageLoadStart = window.pageLoadStart || performance.now();

    // 
    // FUNKCJA POMOCNICZA: Formatowanie czasu w mikrosekundach
    //
    function formatTime(timeInMs) {
        // Zapewnia format '0.0000 ms' - 4 miejsca po przecinku (mikrosekundy)
        return timeInMs.toFixed(4);
    }

    // 
    // FUNKCJA POMOCNICZA: Losowanie milisekund dla symulacji opóźnienia
    //
    function getRandomMs(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    //
    // FUNKCJA GŁÓWNA: Obsługa wszystkich statusów (z sekwencyjną animacją)
    //
    function initializeStatusChecks() {
        const statuses = [
            { id: 'css-status', tech: '.CSS', type: 'loadTime', delay: 0, font: 'font-teko', color: '#00e5ff' },
            { id: 'js-status', tech: '.JS', type: 'loadTime', delay: 100, font: 'font-fira-code', color: '#ffd700' },
            { id: 'php-status', tech: '.PHP', type: 'simulated', minMs: 50, maxMs: 150, delay: 500, font: 'font-playfair', color: '#ff6600' },
            { id: 'sql-status', tech: '.SQL', type: 'simulated', minMs: 100, maxMs: 350, delay: 1000, font: 'font-roboto-mono', color: '#00c3ff', target: 'google.pl' }
        ];

        statuses.forEach(status => {
            const element = document.getElementById(status.id);
            element.classList.add('status-connecting'); // Dodanie klasy do animacji pulsowania

            // Użycie setTimeout do sekwencyjnego uruchomienia testów
            setTimeout(() => {
                let loadTime;
                
                if (status.type === 'loadTime') {
                    // Mierzenie czasu od 'pageLoadStart' do momentu wykonania tej linii
                    loadTime = performance.now() - pageLoadStart; 
                    
                    updateStatus(element, status.tech, loadTime, status.color);

                } else if (status.type === 'simulated') {
                    // Symulacja połączenia serwerowego/bazodanowego
                    const connectionTime = getRandomMs(status.minMs, status.maxMs);
                    
                    // Użycie drugiego setTimeout do symulacji czasu oczekiwania na odpowiedź
                    setTimeout(() => {
                        let message = `${status.tech} - realtime: **Connected** (${connectionTime} ms)`;
                        if (status.target) {
                            message += ` (Target: ${status.target})`;
                        }
                        updateStatus(element, status.tech, connectionTime, '#39ff14', message); // Neon Green
                    }, connectionTime);
                }
            }, status.delay);
        });
    }

    // Aktualizacja elementu statusu
    function updateStatus(element, tech, time, color, customMessage = null) {
        element.classList.remove('status-connecting');
        element.style.color = color;

        if (customMessage) {
            element.innerHTML = customMessage;
        } else {
            // Dla CSS/JS używamy precyzyjnego formatu mikrosekund
            const formattedTime = formatTime(time);
            element.innerHTML = `${tech} - realtime: **Connected** (${formattedTime} ms)`;
        }
    }
    
    //
    // ZARZĄDZANIE WYJŚCIEM JS (KOMUNIKAT I OPCJE)
    //
    const jsOutputSection = document.getElementById('js-output-section');
    let outputText = '.JS - Javascript - works correctly.\n\n';
    
    const options = [
        "1. Sweet kitties from Google [ACCESS: GRANTED]",
        "2. OpenAI's latest model demo [ACCESS: GRANTED]",
        "3. Advanced CSS grid layout example [ACCESS: GRANTED]"
    ];
    
    options.forEach(option => {
        outputText += `[TASK] ${option}\n`;
    });

    const outputDiv = document.createElement('div');
    outputDiv.innerText = outputText;
    jsOutputSection.appendChild(outputDiv);

    //
    // ZEGAR CZASU RZECZYWISTEGO (LEWY DÓŁ)
    //
    const clockElement = document.getElementById('realtime-clock');

    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('pl-PL', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false // Format 24-godzinny
        });
        clockElement.textContent = `SYSTEM TIME: ${timeString}`;
    }

    // Aktualizacja zegara co sekundę
    setInterval(updateClock, 1000);
    updateClock(); // Uruchomienie od razu, by uniknąć opóźnienia

    // Uruchomienie głównej logiki statusów
    initializeStatusChecks();
});