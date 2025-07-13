const msgSearchInput = document.getElementById('messages-search-input');
const msgSearchResults = document.getElementById('messages-search-results');
const msgUserList = document.getElementById('messages-user-list');

function performMessagesSearch() {
    const query = msgSearchInput.value.trim();
    if (query.length >= 1) {
        fetch(`/user_search/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous search results, keep header
                msgSearchResults.innerHTML = '<div class="list-header">Search Results</div>';
                if (data.length > 0) {
                    data.forEach(user => {
                        const div = document.createElement('div');
                        div.classList.add('user-list-item');
                        div.innerHTML = `
                            <img src="${user.profile_image}" alt="${user.username}" class="rounded-circle" style="width: 48px; height: 48px; border: 1px solid #e0e0e0;">
                            <span class="user-name">${user.username}</span>
                            <a href="/messages/${user.id}/" class="btn btn-sm btn-primary ms-auto">View</a>
                        `;
                        msgSearchResults.appendChild(div);
                    });
                } else {
                    msgSearchResults.innerHTML += '<div class="no-users">No users found.</div>';
                }
                msgSearchResults.style.display = 'block';
                msgUserList.style.display = 'block'; // Ensure conversed users remain visible
            })
            .catch(error => {
                msgSearchResults.innerHTML = '<div class="list-header">Search Results</div><div class="no-users text-danger">Error searching users.</div>';
                msgSearchResults.style.display = 'block';
                msgUserList.style.display = 'block';
            });
    } else {
        msgSearchResults.style.display = 'none';
        msgSearchResults.innerHTML = '<div class="list-header">Search Results</div>';
        msgUserList.style.display = 'block';
    }
}

if (msgSearchInput) {
    msgSearchInput.addEventListener('input', performMessagesSearch);
}