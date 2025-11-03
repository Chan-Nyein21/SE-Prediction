// Admin Dashboard JavaScript

// Search functionality
document.getElementById('searchInput')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const tableRows = document.querySelectorAll('#usersTableBody tr');
    
    tableRows.forEach(row => {
        const username = row.querySelector('.user-name')?.textContent.toLowerCase() || '';
        const email = row.cells[1]?.textContent.toLowerCase() || '';
        
        if (username.includes(searchTerm) || email.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Accept user function
function acceptUser(email) {
    if (confirm(`Are you sure you want to accept user: ${email}?`)) {
        // TODO: Send request to backend to accept user
        fetch('/admin/accept-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => {
            if (response.status === 403) {
                alert('Your session has expired. Please login again.');
                window.location.href = '/login';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                alert('User accepted successfully!');
                location.reload();
            } else if (data) {
                alert('Failed to accept user: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while accepting the user.');
        });
    }
}

// Delete user function
function deleteUser(email) {
    if (confirm(`Are you sure you want to delete user: ${email}? This action cannot be undone.`)) {
        // TODO: Send request to backend to delete user
        fetch('/admin/delete-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email })
        })
        .then(response => {
            if (response.status === 403) {
                alert('Your session has expired. Please login again.');
                window.location.href = '/login';
                return;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.success) {
                alert('User deleted successfully!');
                location.reload();
            } else if (data) {
                alert('Failed to delete user: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the user.');
        });
    }
}
