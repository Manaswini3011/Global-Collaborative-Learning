// Dashboard JavaScript

let currentRoomId = null;
let messagePollInterval = null;
let currentUserId = null;

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserProfile();
    await loadDashboardData();
    await loadTeams();
    await loadProjects();
    await loadRooms();
    await loadProgress();
    await loadResources();
    await loadInvitations();
});

// Section Navigation
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionName).classList.add('active');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load section-specific data
    if (sectionName === 'discover') {
        loadDiscoverUsers();
    } else if (sectionName === 'invitations') {
        loadInvitations();
    }
}

// Load User Profile
async function loadUserProfile() {
    try {
        const response = await fetch('/api/user/profile');
        if (response.ok) {
            const user = await response.json();
            currentUserId = user.user_id;
            document.getElementById('userName').textContent = user.full_name || user.username;
            document.getElementById('userPoints').textContent = user.points || 0;
            document.getElementById('userLevel').textContent = user.level || 1;
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Load Dashboard Data
async function loadDashboardData() {
    await loadRecommendations();
    await loadTeamCount();
}

async function loadTeamCount() {
    try {
        const response = await fetch('/api/teams');
        if (response.ok) {
            const teams = await response.json();
            document.getElementById('teamCount').textContent = teams.length || 0;
        }
    } catch (error) {
        console.error('Error loading teams count:', error);
    }
}

// Load Recommendations
async function loadRecommendations() {
    try {
        const response = await fetch('/api/recommendations');
        if (response.ok) {
            const recommendations = await response.json();
            const container = document.getElementById('recommendationsList');
            container.innerHTML = '';
            
            if (recommendations.length === 0) {
                container.innerHTML = '<p class="empty-state">No recommendations available</p>';
                return;
            }
            
            recommendations.forEach(rec => {
                const item = document.createElement('div');
                item.className = 'recommendation-item';
                item.innerHTML = `
                    <h4>${rec.title}</h4>
                    <p>${rec.description}</p>
                    <span class="badge">${rec.difficulty_level}</span>
                `;
                item.onclick = () => createProjectFromRecommendation(rec);
                container.appendChild(item);
            });
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

function createProjectFromRecommendation(rec) {
    showCreateProjectModal(rec);
}

// Load Teams
async function loadTeams() {
    try {
        const response = await fetch('/api/teams');
        if (response.ok) {
            const teams = await response.json();
            const container = document.getElementById('teamsList');
            container.innerHTML = '';
            
            if (teams.length === 0) {
                container.innerHTML = '<p class="empty-state">No teams yet. Create your first team!</p>';
                return;
            }
            
            for (const team of teams) {
                // Load team members
                const membersResponse = await fetch(`/api/teams/${team.team_id}/members`);
                const members = membersResponse.ok ? await membersResponse.json() : [];
                
                const card = document.createElement('div');
                card.className = 'team-card';
                card.innerHTML = `
                    <h3>${team.team_name}</h3>
                    <p>${team.description || 'No description'}</p>
                    <div class="team-members-preview">
                        <strong>Members:</strong>
                        <div class="members-list">
                            ${members.map(m => `<span class="member-badge">${m.full_name} (${m.country})</span>`).join('')}
                        </div>
                    </div>
                    <div class="team-meta">
                        <span>${team.member_count || members.length} members</span>
                        <span class="team-status ${team.status}">${team.status}</span>
                    </div>
                `;
                container.appendChild(card);
            }
        }
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

// Load Projects
async function loadProjects() {
    try {
        const response = await fetch('/api/projects');
        if (response.ok) {
            const projects = await response.json();
            const container = document.getElementById('projectsList');
            container.innerHTML = '';
            
            if (projects.length === 0) {
                container.innerHTML = '<p class="empty-state">No projects yet. Create your first project!</p>';
                return;
            }
            
            projects.forEach(project => {
                const card = document.createElement('div');
                card.className = 'project-card';
                card.innerHTML = `
                    <h3>${project.project_name}</h3>
                    <p>${project.description || 'No description'}</p>
                    <p><strong>Team:</strong> ${project.team_name || 'No team'}</p>
                    <p><strong>Status:</strong> ${project.status}</p>
                `;
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

// Load Rooms
async function loadRooms() {
    try {
        const response = await fetch('/api/rooms');
        if (response.ok) {
            const rooms = await response.json();
            const container = document.getElementById('roomsList');
            container.innerHTML = '';
            
            if (rooms.length === 0) {
                container.innerHTML = '<p class="empty-state">No discussion rooms yet. Create one!</p>';
                return;
            }
            
            rooms.forEach(room => {
                const card = document.createElement('div');
                card.className = 'room-card';
                card.innerHTML = `
                    <h3>${room.room_name}</h3>
                    <p><strong>Team:</strong> ${room.team_name || 'General'}</p>
                    <p><strong>Project:</strong> ${room.project_name || 'None'}</p>
                `;
                card.onclick = () => openRoom(room.room_id, room.room_name);
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

// Open Discussion Room
async function openRoom(roomId, roomName) {
    currentRoomId = roomId;
    document.getElementById('roomTitle').textContent = roomName;
    document.getElementById('roomModal').classList.add('active');
    
    // Load room members
    await loadRoomMembers(roomId);
    loadMessages(roomId);
    
    // Start polling for new messages
    if (messagePollInterval) {
        clearInterval(messagePollInterval);
    }
    messagePollInterval = setInterval(() => loadMessages(roomId), 2000);
}

// Load room members
async function loadRoomMembers(roomId) {
    try {
        // Get team_id from room
        const roomsResponse = await fetch('/api/rooms');
        if (roomsResponse.ok) {
            const rooms = await roomsResponse.json();
            const room = rooms.find(r => r.room_id === roomId);
            if (room && room.team_id) {
                const membersResponse = await fetch(`/api/teams/${room.team_id}/members`);
                if (membersResponse.ok) {
                    const members = await membersResponse.json();
                    const container = document.getElementById('roomMembers');
                    container.innerHTML = `
                        <div class="room-members-header">
                            <strong>Team Members:</strong>
                            ${members.map(m => `<span class="member-tag">${m.full_name} (${m.country}) - ${m.role}</span>`).join('')}
                        </div>
                    `;
                }
            }
        }
    } catch (error) {
        console.error('Error loading room members:', error);
    }
}

function closeRoomModal() {
    document.getElementById('roomModal').classList.remove('active');
    if (messagePollInterval) {
        clearInterval(messagePollInterval);
    }
    currentRoomId = null;
}

async function loadMessages(roomId) {
    try {
        const response = await fetch(`/api/rooms/${roomId}/messages`);
        if (response.ok) {
            const messages = await response.json();
            const container = document.getElementById('messagesContainer');
            const currentScroll = container.scrollTop;
            const wasAtBottom = container.scrollHeight - container.scrollTop <= container.clientHeight + 100;
            
            container.innerHTML = '';
            
            if (messages.length === 0) {
                container.innerHTML = '<p class="empty-state">No messages yet. Start the conversation!</p>';
                return;
            }
            
            messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${msg.user_id === getCurrentUserId() ? 'own' : 'other'}`;
                
                // Use display_text if available (translated), otherwise use original
                const displayText = msg.display_text || msg.message_text;
                const originalText = msg.original_text || msg.message_text;
                const isTranslated = msg.is_translated || false;
                const originalLang = msg.original_language || 'en';
                const displayLang = msg.display_language || 'en';
                
                // Build message header with language info
                let headerText = `${msg.full_name || msg.username} (${msg.country || 'Unknown'}) - ${new Date(msg.created_at).toLocaleTimeString()}`;
                if (isTranslated && originalLang !== displayLang) {
                    headerText += ` <span class="lang-badge">${originalLang.toUpperCase()} → ${displayLang.toUpperCase()}</span>`;
                }
                
                messageDiv.innerHTML = `
                    <div class="message-header">${headerText}</div>
                    <div class="message-text">${escapeHtml(displayText)}</div>
                    ${isTranslated && originalText !== displayText ? 
                        `<div class="message-original" onclick="toggleOriginal(this)" title="Click to view original">
                            <span class="original-label">Original (${originalLang.toUpperCase()}):</span>
                            <span class="original-text" style="display: none;">${escapeHtml(originalText)}</span>
                        </div>` : ''}
                `;
                container.appendChild(messageDiv);
            });
            
            // Scroll to bottom if user was at bottom
            if (wasAtBottom) {
                container.scrollTop = container.scrollHeight;
            }
        } else {
            const error = await response.json();
            if (response.status === 403) {
                const container = document.getElementById('messagesContainer');
                container.innerHTML = `<p class="empty-state" style="color: var(--accent-color);">${error.error}</p>`;
            }
        }
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function toggleOriginal(element) {
    const originalText = element.querySelector('.original-text');
    if (originalText) {
        originalText.style.display = originalText.style.display === 'none' ? 'block' : 'none';
    }
}

function getCurrentUserId() {
    return currentUserId;
}

function handleMessageKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const messageText = input.value.trim();
    
    if (!messageText || !currentRoomId) return;
    
    try {
        const response = await fetch(`/api/rooms/${currentRoomId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message_text: messageText })
        });
        
        if (response.ok) {
            input.value = '';
            loadMessages(currentRoomId);
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to send message');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Error sending message');
    }
}

// Load Progress
async function loadProgress() {
    try {
        const response = await fetch('/api/progress');
        if (response.ok) {
            const progress = await response.json();
            const container = document.getElementById('progressList');
            container.innerHTML = '';
            
            if (progress.length === 0) {
                container.innerHTML = '<p class="empty-state">No progress tracked yet</p>';
                return;
            }
            
            progress.forEach(item => {
                const progressDiv = document.createElement('div');
                progressDiv.className = 'progress-item';
                progressDiv.innerHTML = `
                    <h4>${item.task_description || 'Task'}</h4>
                    <p><strong>Project:</strong> ${item.project_name || 'N/A'}</p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${item.completion_percentage}%"></div>
                    </div>
                    <p>${item.completion_percentage}% Complete</p>
                `;
                container.appendChild(progressDiv);
            });
        }
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

// Load Resources
async function loadResources() {
    try {
        const response = await fetch('/api/resources');
        if (response.ok) {
            const resources = await response.json();
            const container = document.getElementById('resourcesList');
            container.innerHTML = '';
            
            if (resources.length === 0) {
                container.innerHTML = '<p class="empty-state">No resources shared yet</p>';
                return;
            }
            
            resources.forEach(resource => {
                const card = document.createElement('div');
                card.className = 'resource-card';
                card.innerHTML = `
                    <h4>${resource.resource_name}</h4>
                    <p>${resource.description || 'No description'}</p>
                    <p><strong>Type:</strong> ${resource.resource_type}</p>
                    <p><strong>Uploaded by:</strong> ${resource.uploaded_by_name}</p>
                    ${resource.resource_url ? `<a href="${resource.resource_url}" target="_blank">View Resource</a>` : ''}
                `;
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error loading resources:', error);
    }
}

// Load Achievements
async function loadAchievements() {
    try {
        const response = await fetch('/api/achievements');
        if (response.ok) {
            const achievements = await response.json();
            const container = document.getElementById('achievementsList');
            container.innerHTML = '';
            
            if (achievements.length === 0) {
                container.innerHTML = '<p class="empty-state">No achievements yet</p>';
                return;
            }
            
            achievements.forEach(achievement => {
                const item = document.createElement('div');
                item.className = 'achievement-item';
                item.innerHTML = `
                    <h4>${achievement.achievement_name}</h4>
                    <div class="points">+${achievement.points_earned} points</div>
                `;
                container.appendChild(item);
            });
        }
    } catch (error) {
        console.error('Error loading achievements:', error);
    }
}

// Modal Functions
function showCreateTeamModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Create New Team</h2>
        <form onsubmit="createTeam(event)">
            <div class="form-group">
                <label>Team Name</label>
                <input type="text" id="teamName" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="teamDescription" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Create Team</button>
        </form>
    `;
    document.getElementById('modalOverlay').classList.add('active');
}

function showCreateProjectModal(recommendation = null) {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Create New Project</h2>
        <form onsubmit="createProject(event)">
            <div class="form-group">
                <label>Project Name</label>
                <input type="text" id="projectName" value="${recommendation ? recommendation.title : ''}" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="projectDescription" rows="3">${recommendation ? recommendation.description : ''}</textarea>
            </div>
            <div class="form-group">
                <label>Team</label>
                <select id="projectTeam" required>
                    <option value="">Select a team</option>
                </select>
            </div>
            <div class="form-group">
                <label>Difficulty Level</label>
                <select id="projectDifficulty">
                    <option value="easy">Easy</option>
                    <option value="medium" selected>Medium</option>
                    <option value="hard">Hard</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Create Project</button>
        </form>
    `;
    
    // Load teams for dropdown
    loadTeamsForProject();
    
    document.getElementById('modalOverlay').classList.add('active');
}

async function loadTeamsForProject() {
    try {
        const response = await fetch('/api/teams');
        if (response.ok) {
            const teams = await response.json();
            const select = document.getElementById('projectTeam');
            teams.forEach(team => {
                const option = document.createElement('option');
                option.value = team.team_id;
                option.textContent = team.team_name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

function showCreateRoomModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Create Discussion Room</h2>
        <form onsubmit="createRoom(event)">
            <div class="form-group">
                <label>Room Name</label>
                <input type="text" id="roomName" required>
            </div>
            <div class="form-group">
                <label>Team</label>
                <select id="roomTeam">
                    <option value="">Select a team</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Create Room</button>
        </form>
    `;
    
    loadTeamsForRoom();
    document.getElementById('modalOverlay').classList.add('active');
}

async function loadTeamsForRoom() {
    try {
        const response = await fetch('/api/teams');
        if (response.ok) {
            const teams = await response.json();
            const select = document.getElementById('roomTeam');
            teams.forEach(team => {
                const option = document.createElement('option');
                option.value = team.team_id;
                option.textContent = team.team_name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

function showUploadResourceModal() {
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Upload Resource</h2>
        <form onsubmit="uploadResource(event)">
            <div class="form-group">
                <label>Resource Name</label>
                <input type="text" id="resourceName" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="resourceDescription" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>Resource URL</label>
                <input type="url" id="resourceUrl" required>
            </div>
            <div class="form-group">
                <label>Type</label>
                <select id="resourceType">
                    <option value="file">File</option>
                    <option value="link">Link</option>
                    <option value="document">Document</option>
                    <option value="video">Video</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Upload</button>
        </form>
    `;
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
}

// Create Functions
async function createTeam(event) {
    event.preventDefault();
    const teamData = {
        team_name: document.getElementById('teamName').value,
        description: document.getElementById('teamDescription').value
    };
    
    try {
        const response = await fetch('/api/teams', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(teamData)
        });
        
        if (response.ok) {
            closeModal();
            loadTeams();
            loadTeamCount();
        } else {
            alert('Failed to create team');
        }
    } catch (error) {
        console.error('Error creating team:', error);
    }
}

async function createProject(event) {
    event.preventDefault();
    const projectData = {
        project_name: document.getElementById('projectName').value,
        description: document.getElementById('projectDescription').value,
        team_id: parseInt(document.getElementById('projectTeam').value),
        difficulty_level: document.getElementById('projectDifficulty').value
    };
    
    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });
        
        if (response.ok) {
            closeModal();
            loadProjects();
        } else {
            alert('Failed to create project');
        }
    } catch (error) {
        console.error('Error creating project:', error);
    }
}

async function createRoom(event) {
    event.preventDefault();
    const roomData = {
        room_name: document.getElementById('roomName').value,
        team_id: document.getElementById('roomTeam').value ? parseInt(document.getElementById('roomTeam').value) : null
    };
    
    try {
        const response = await fetch('/api/rooms', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(roomData)
        });
        
        if (response.ok) {
            closeModal();
            loadRooms();
        } else {
            alert('Failed to create room');
        }
    } catch (error) {
        console.error('Error creating room:', error);
    }
}

async function uploadResource(event) {
    event.preventDefault();
    const resourceData = {
        resource_name: document.getElementById('resourceName').value,
        description: document.getElementById('resourceDescription').value,
        resource_url: document.getElementById('resourceUrl').value,
        resource_type: document.getElementById('resourceType').value
    };
    
    try {
        const response = await fetch('/api/resources', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(resourceData)
        });
        
        if (response.ok) {
            closeModal();
            loadResources();
        } else {
            alert('Failed to upload resource');
        }
    } catch (error) {
        console.error('Error uploading resource:', error);
    }
}

// Logout
async function handleLogout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        window.location.href = '/';
    } catch (error) {
        console.error('Error logging out:', error);
        window.location.href = '/';
    }
}

// ==================== USER DISCOVERY ====================

async function loadDiscoverUsers() {
    try {
        const response = await fetch('/api/users/discover');
        if (response.ok) {
            const users = await response.json();
            const container = document.getElementById('discoverUsersList');
            container.innerHTML = '';
            
            if (users.length === 0) {
                container.innerHTML = '<p class="empty-state">No users found</p>';
                return;
            }
            
            users.forEach(user => {
                const card = document.createElement('div');
                card.className = 'user-card';
                card.innerHTML = `
                    <div class="user-card-header">
                        <h3>${user.full_name}</h3>
                        <div class="compatibility-badge">Match: ${user.compatibility_score}</div>
                    </div>
                    <div class="user-card-body">
                        <p><strong>Country:</strong> ${user.country || 'Unknown'}</p>
                        <p><strong>Language:</strong> ${user.language || 'Unknown'}</p>
                        <p><strong>Skills:</strong> ${user.skills || 'None'}</p>
                        <p><strong>Interests:</strong> ${user.interests || 'None'}</p>
                        ${user.skill_matches && user.skill_matches.length > 0 ? 
                            `<p class="match-info"><strong>Matching Skills:</strong> ${user.skill_matches.join(', ')}</p>` : ''}
                        ${user.interest_matches && user.interest_matches.length > 0 ? 
                            `<p class="match-info"><strong>Matching Interests:</strong> ${user.interest_matches.join(', ')}</p>` : ''}
                        <p><strong>Points:</strong> ${user.points || 0} | <strong>Level:</strong> ${user.level || 1}</p>
                    </div>
                    <div class="user-card-actions">
                        ${user.already_teamed ? 
                            '<span class="badge">Already in a team together</span>' :
                            '<button onclick="showInviteUserModal(' + user.user_id + ', \'' + user.full_name + '\')" class="btn btn-primary btn-sm">Invite to Team</button>'
                        }
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

function showInviteUserModal(userId, userName) {
    // First load teams
    fetch('/api/teams')
        .then(response => response.json())
        .then(teams => {
            if (teams.length === 0) {
                alert('You need to create a team first!');
                return;
            }
            
            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = `
                <h2>Invite ${userName} to Team</h2>
                <form onsubmit="sendInvitation(event, ${userId})">
                    <div class="form-group">
                        <label>Select Team</label>
                        <select id="inviteTeamId" required>
                            ${teams.map(team => `<option value="${team.team_id}">${team.team_name}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Message (Optional)</label>
                        <textarea id="inviteMessage" rows="3" placeholder="Add a personal message..."></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send Invitation</button>
                </form>
            `;
            document.getElementById('modalOverlay').classList.add('active');
        })
        .catch(error => {
            console.error('Error loading teams:', error);
            alert('Error loading teams');
        });
}

async function sendInvitation(event, userId) {
    event.preventDefault();
    const invitationData = {
        team_id: parseInt(document.getElementById('inviteTeamId').value),
        to_user_id: userId,
        message: document.getElementById('inviteMessage').value
    };
    
    try {
        const response = await fetch('/api/invitations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(invitationData)
        });
        
        if (response.ok) {
            closeModal();
            alert('Invitation sent successfully!');
            loadInvitations();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to send invitation');
        }
    } catch (error) {
        console.error('Error sending invitation:', error);
        alert('Error sending invitation');
    }
}

// ==================== INVITATIONS ====================

async function loadInvitations() {
    try {
        const response = await fetch('/api/invitations');
        if (response.ok) {
            const data = await response.json();
            
            // Display received invitations
            const receivedContainer = document.getElementById('receivedInvitations');
            receivedContainer.innerHTML = '';
            
            if (data.received && data.received.length > 0) {
                data.received.forEach(inv => {
                    const card = document.createElement('div');
                    card.className = 'invitation-card';
                    card.innerHTML = `
                        <div class="invitation-header">
                            <h4>${inv.team_name}</h4>
                            <span class="invitation-status pending">Pending</span>
                        </div>
                        <p><strong>From:</strong> ${inv.from_user_name}</p>
                        ${inv.message ? `<p>${inv.message}</p>` : ''}
                        <div class="invitation-actions">
                            <button onclick="acceptInvitation(${inv.invitation_id})" class="btn btn-primary btn-sm">Accept</button>
                            <button onclick="rejectInvitation(${inv.invitation_id})" class="btn btn-secondary btn-sm">Reject</button>
                        </div>
                    `;
                    receivedContainer.appendChild(card);
                });
            } else {
                receivedContainer.innerHTML = '<p class="empty-state">No received invitations</p>';
            }
            
            // Display sent invitations
            const sentContainer = document.getElementById('sentInvitations');
            sentContainer.innerHTML = '';
            
            if (data.sent && data.sent.length > 0) {
                data.sent.forEach(inv => {
                    const card = document.createElement('div');
                    card.className = 'invitation-card';
                    card.innerHTML = `
                        <div class="invitation-header">
                            <h4>${inv.team_name}</h4>
                            <span class="invitation-status ${inv.status}">${inv.status}</span>
                        </div>
                        <p><strong>To:</strong> ${inv.to_user_name}</p>
                        ${inv.message ? `<p>${inv.message}</p>` : ''}
                    `;
                    sentContainer.appendChild(card);
                });
            } else {
                sentContainer.innerHTML = '<p class="empty-state">No sent invitations</p>';
            }
        }
    } catch (error) {
        console.error('Error loading invitations:', error);
    }
}

async function acceptInvitation(invitationId) {
    try {
        const response = await fetch(`/api/invitations/${invitationId}/accept`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Invitation accepted! You are now a team member.');
            loadInvitations();
            loadTeams();
            loadTeamCount();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to accept invitation');
        }
    } catch (error) {
        console.error('Error accepting invitation:', error);
        alert('Error accepting invitation');
    }
}

async function rejectInvitation(invitationId) {
    try {
        const response = await fetch(`/api/invitations/${invitationId}/reject`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Invitation rejected');
            loadInvitations();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to reject invitation');
        }
    } catch (error) {
        console.error('Error rejecting invitation:', error);
        alert('Error rejecting invitation');
    }
}

