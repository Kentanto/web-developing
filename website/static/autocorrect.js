document.addEventListener("DOMContentLoaded", function() {
    const checkModifyBtn = document.getElementById("check-modify-btn");
    const killPersonBtn = document.getElementById("kill-person-btn");

    var isProgrammaticInput = false;

checkModifyBtn.addEventListener("click", function() {
    initializeAutocorrect("person_name", "check-spell-suggestions");});
killPersonBtn.addEventListener("click", function() {
    initializeAutocorrect('target_person', "kill-spell-suggestions");
    initializeAutocorrect('killer', "kill-spell-suggestions");});

function initializeAutocorrect(inputId, inputSuggestion) {
    var inputField = document.getElementById(inputId);
    var inputSuggestions = document.getElementById(inputSuggestion);
    if (!inputField) return;
    
    inputField.addEventListener('input', function() {
        var inputValue = this.value;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/get_person_info', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    document.getElementById('person-info').innerHTML = response.html;
                } else {
                    console.error('Request failed:', xhr.status);
                }
            }
        };
        xhr.send(JSON.stringify({ person_name: inputValue }));

        if (!isProgrammaticInput) {
            var spellCheckXhr = new XMLHttpRequest();
            spellCheckXhr.open('POST', '/spell_check', true);
            spellCheckXhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            spellCheckXhr.onreadystatechange = function() {
                if (spellCheckXhr.readyState === XMLHttpRequest.DONE) {
                    if (spellCheckXhr.status === 200) {
                        var spellCheckResponse = JSON.parse(spellCheckXhr.responseText);
                        var suggestions = spellCheckResponse.suggestions;
                        if (suggestions.length > 0) {
                            inputSuggestions.innerHTML = '';
                            suggestions.forEach(function(suggestion) {
                                var listItem = document.createElement('div');
                                listItem.textContent = suggestion[0];
                                inputSuggestions.appendChild(listItem);
                            });
                        }
                    } else {
                        console.error('Spell check request failed:', spellCheckXhr.status);
                    }
                }
            };
            spellCheckXhr.send('word=' + inputValue);
        }
    });

    inputField.addEventListener('keydown', function(event) {
        if (event.key === 'Tab' ) {
            event.preventDefault();
            var topSuggestion = inputSuggestions.firstElementChild.textContent;
            var currentValue = this.value;
            var caretPosition = this.selectionStart;
            var words = currentValue.split(' ');
            var lastWordIndex = words.length - 1;
            words[lastWordIndex] = topSuggestion;
            var newValue = words.join(' ');
            this.value = newValue;
            this.setSelectionRange(caretPosition, caretPosition);
            isProgrammaticInput = true;
            var inputEvent = new Event('input', {
                bubbles: true,
                cancelable: true,
            });
            this.dispatchEvent(inputEvent);
            isProgrammaticInput = false;
        }
    });
}
});