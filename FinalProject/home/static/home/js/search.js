document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('searchInput');
  const suggestionBox = document.getElementById('resultsBox');

  input.addEventListener('input', function () {
    const query = input.value;

    if (query.length > 1) {
      fetch(`/live-search/?q=${query}`)
        .then(response => response.json())
        .then(data => {
          suggestionBox.innerHTML = '';

          data.results.forEach(album => {
            const resultItem = document.createElement('a');
            resultItem.classList.add(
              'list-group-item',
              'list-group-item-action',
              'd-flex',
              'align-items-center'
            );
            resultItem.href = `/vinyl/${album.id}/`;

            resultItem.innerHTML = `
              <img src="${album.image}" alt="${album.title}" class="me-3 rounded" style="width: 50px; height: 50px; object-fit: cover;">
              <div>
                <div><strong>${album.title}</strong></div>
                <small class="text-muted">${album.artist}</small>
              </div>
            `;

            suggestionBox.appendChild(resultItem);
          });

          suggestionBox.classList.remove('d-none');
        });
    } else {
      suggestionBox.classList.add('d-none');
    }
  });

  //hide suggestion box
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#searchInput') && !e.target.closest('#resultsBox')) {
      suggestionBox.classList.add('d-none');
    }
  });
});
