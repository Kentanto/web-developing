document.addEventListener('DOMContentLoaded', function() {
    const filterCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    const peopleElements = document.querySelectorAll('.person');

    function filterPeople() {
        const showDead = document.getElementById('filter-dead').checked;
        const showAlive = document.getElementById('filter-alive').checked;

        peopleElements.forEach(person => {
            const status = person.dataset.status;
            if (showDead && showAlive) {
                person.style.display = 'block';
                if (status.includes('dead')) {
                    person.classList.add('dead');
                } else {
                    person.classList.remove('dead');
                }
            } else if (showDead && status.includes('dead')) {
                person.style.display = 'block';
                person.classList.add('dead');
            } else if (showAlive && !status.includes('dead')) {
                person.style.display = 'block';
                person.classList.remove('dead');
            } else {
                person.style.display = 'none';
                person.classList.remove('dead');
            }
        });
    }

    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterPeople);
    });

    filterPeople();
});