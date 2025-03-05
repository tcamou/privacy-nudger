function removeAccess(fileId, permissionId) {
    fetch(`/remove-access?fileId=${fileId}&permissionId=${permissionId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert("Access removed successfully!");
            location.reload(); // Refresh the page to reflect changes
        });
}

function disableLinkSharing(fileId) {
    console.log(fileId);
    fetch(`/disable-link-sharing?fileId=${fileId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert("Link sharing disabled successfully!");
                location.reload(); // Refresh the page to reflect changes
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(error => {
            alert("An error occurred: " + error.message);
        });
}