# Changelog - Team Collaboration Features

## New Features Added

### 1. User Discovery with AI-Guided Skill Matching
- **Endpoint**: `GET /api/users/discover`
- **Feature**: Users can discover other users based on skill and interest compatibility
- **AI Matching**: Calculates compatibility scores based on:
  - Skill matches (weighted 2x)
  - Interest matches
  - Shows matching skills and interests
- **UI**: New "Discover Users" section in dashboard
- **Display**: Shows user cards with compatibility scores, skills, interests, and country

### 2. Team Invitation System
- **Database**: New `team_invitations` table added
- **Endpoints**:
  - `GET /api/invitations` - Get sent and received invitations
  - `POST /api/invitations` - Send team invitation
  - `POST /api/invitations/<id>/accept` - Accept invitation
  - `POST /api/invitations/<id>/reject` - Reject invitation
- **Workflow**:
  1. User discovers another user
  2. User selects a team and sends invitation
  3. Invited user receives notification
  4. Invited user can accept or reject
  5. On acceptance, user is added to team and earns 50 points

### 3. Collaboration Restrictions
- **Security**: Only team members can collaborate
- **Protected Features**:
  - Discussion rooms: Only team members can view/send messages
  - Projects: Only team members can create projects for a team
  - Rooms: Only team members can create rooms for a team
- **Error Handling**: Returns 403 Forbidden with clear error messages

### 4. Team Members Display
- **Teams Section**: Shows all team members with their roles
- **Discussion Rooms**: Displays team members in the room header
- **Member Info**: Shows name, country, and role for each member

### 5. Enhanced Message Display
- **Fixed**: Messages now properly display text content
- **Features**:
  - Shows sender name, country, and timestamp
  - Displays translated text (when available)
  - Proper HTML escaping for security
  - Auto-scroll to bottom for new messages
  - Clear error messages for non-team members

## Database Changes

### New Table: `team_invitations`
```sql
CREATE TABLE team_invitations (
    invitation_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    from_user_id INT NOT NULL,
    to_user_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP NULL
);
```

## UI Updates

### New Sections
1. **Discover Users**: Grid view of users with compatibility scores
2. **Invitations**: Separate sections for received and sent invitations

### Enhanced Sections
1. **Teams**: Now shows team members list
2. **Discussion Rooms**: Shows team members in room header
3. **Messages**: Improved display with timestamps and translations

### New UI Components
- User cards with compatibility badges
- Invitation cards with status indicators
- Team member badges and tags
- Room members header

## Security Improvements

1. **Team Membership Verification**: All collaboration endpoints check team membership
2. **Invitation Validation**: Prevents duplicate invitations and invalid states
3. **HTML Escaping**: Prevents XSS attacks in message display

## How to Use

### Discovering Users
1. Navigate to "Discover Users" section
2. Browse users sorted by compatibility score
3. View matching skills and interests
4. Click "Invite to Team" for compatible users

### Sending Invitations
1. Select a user from discovery
2. Choose a team to invite them to
3. Optionally add a personal message
4. Send invitation

### Managing Invitations
1. Go to "Invitations" section
2. View received invitations in the left panel
3. Accept or reject invitations
4. View sent invitations status in the right panel

### Collaborating
1. Only team members can:
   - View and send messages in team discussion rooms
   - Create projects for the team
   - Create discussion rooms for the team
   - Access team resources

## Migration Instructions

1. **Update Database**:
   ```sql
   -- Run the updated schema.sql or add the team_invitations table manually
   ```

2. **Restart Application**:
   ```bash
   python app.py
   ```

3. **Test Features**:
   - Create a team
   - Discover users
   - Send invitations
   - Accept invitations
   - Test collaboration restrictions

## Notes

- Invitation system prevents users from being in multiple teams together (can be modified)
- Compatibility scoring can be adjusted in the `discover_users()` function
- Points awarded for accepting invitations: 50 (configurable)
- All collaboration features now require team membership

