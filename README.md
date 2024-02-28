### URL Data

Main URL : ```https://snippify-backend.onrender.com/```
Test URL : ```https://snippify-backend.onrender.com/api/test//```
Admin URL : ```https://snippify-backend.onrender.com/admin//```

### Admin Credentials
Email : admin@mail.com
Username : admin
Password : admin123


### Features

1. Must Haves
		
	1. **Code Sharing:**
	   - Users can create and share code snippets.
	   - Display language and the number of lines for each snippet.
	   - CRUD operations with public and private visibility options.
	
	2. **Sharing Options:**
	   - Shareable links for snippets.
	   - Public, open-for-all, and selective sharing (GitHub Gist).
	   - Shorten link option.
	
	3. **Code to Image:**
	   - Convert code snippets to shareable images (similar to carbon.now.sh).
	
	4. **Engagement Features:**
	   - Comments on snippets.
	   - Reactions (upvote and downvote) for snippets.
	
	5. **User Profile:**
	   - Profile page for users/developers.
	   - Lists all public and private snippets.
	   - Analytics for each snippet.
	
	6. **Advanced Search:**
	   - GitHub-like advanced search functionality.
	   - Filter search results by folder, users, language, and specific topics.
	
	7. **Code Upload Options:**
	   - Upload code as a file.
	   - Import from GitHub Gist.
	
	8. **Favorites:**
	   - Add snippets to favorites.

2. Good to Have		
	1. **Code Collaboration:**
	   - Real-time collaboration for writing and viewing code.
	   - Similar to Figma or Google Docs collaboration features.
	
	2. **Version Control System (VCS):**
	   - GitHub-like VCS for snippets.
	   - Includes snippet title, commit message, date, changes, etc.
	
	3. **Code Assistance:**
	   - ChatGPT-like chatbot feature.
	   - Provides insights about code.
	   - Allows users to ask for improvements and reviews.
	   - Generate comments and tests
---

### Models and Schema

1. Snippet

 ```
	 type SnippetType = {
	  snippetId: number | string; // Use either number or uuid,         based on your preference
	  title: string;
	  description : string;
	  language: string[]; // Array of supported languages
	  createdAt: Date;
	  updatedAt: Date;
	  author: string;
	  owner: UserIDType; // Assuming UserIDType is a predefined         type for user identification
	  visibility: 'public' | 'private'; // Enum for visibility
	  upvote: {
	    count: number;
	    users: Array<User>; // Assuming User is a predefined type         for user information
	  };
	  comments: `Array<CommentType>`;
	  codes: `Array<CodeType>`
	 };
 
 ```

2. Code

	```
		type CodeType = {
		  title: string; // Name displayed on the homepage
		  fileNameWithExtension: string; // Name of the code file           with extension
		  language: string[] | string; // String enum or array of           supported languages
		  createdAt: Date;
		  updatedAt: Date;
		  visibility: 'public' | 'private'; // Enum for visibility
		  codeContent: string; // Assuming "code type" refers to            the actual code content
		  numberOfLines: number;
	    };
	```

3. Comments

```
		type CommentType = {
			  id: number | string; // Use either number or uuid, based            on your preference
			  author: string;
			  createdAt: Date;
			  commentText: string;
			  // reactions and replies to comment can be added later on
		};
		
```

4. User
```
		type UserType = {
		  id: number | string; // Use either number or uuid,                based on your preference
		  name: string;
		  username: string;
		  email: string; // Assuming you have a predefined type             for email
		  imageURI: string; // URL for user image
		  numberOfSnippets: {
		    public: number;
		    private: number;
		  };
		  snippets: Array<SnippetType>; // Assuming SnippetType             is the type for snippets
		  bio: string;
		  techStack: Array<string>; // Array of technology terms
		};
```
---

### Screens
Certainly! I'll integrate the information from the previous response with the new details you've provided:

#### Authentication Screens:
1. **Register:**
   - Email and Password (Verified Email)
   - GitHub
   - Google

   Optional:
   - Forgot Password
   - Reset Password

   _Register Page:_
   - Form for username, email, password.

2. **Login:**
   - Email and Password
   - GitHub
   - Google

   Optional:
   - Forgot Password
   - Reset Password

   _Login Page:_
   - Form for username, email, password.

#### Sidebar:
   - Style similar to YouTube and Appwrite.
   - **Tabs:**
      1. Home (Feed for users, popular and recent)
      2. User profile to navigate to user profile
      3. Create a new snippet
      4. Notification for user's snippets
      5. [Placeholder for additional tab]

#### TopBar:
   - Search bar
   - Logo of the App
   - User Photo with an option for logout and user settings

#### HomePage:
   - **Components:**
      - Sidebar
      - Topbar
      - Feed-like UI to display the snippets in a card-like format with hover effect.
      - Search with features to filter snippets with different options.
    
---

### APIs


#### `Authentication APIs`:
1. **Registration:**
   - Email and Password
   - Github
   - Google

2. **Login:**
   - Users can log in via email, GitHub, and Google.

3. **Account Activation** 

4. **Reset Password**

5. **User Profile Edit:**
   - Edit details like name, email, change password, photo, bio, tech.

#### Snippet APIs:
1. **Create/Edit:**
   - API to create a snippet with the following fields:
      - Title
      - Description
      - Image (optional)
      - Content
      - File Name
      - Language
      - Visibility of snippet
   - The API should support adding more than one snippet.

2. **Delete API:**
   - To delete an entire snippet.
   - To delete a particular snippet in a collection.

3. **Read:**
   - Option to show snippets based on filters like language, type, etc.
   - Sorting options:
      - All
      - Based on filters (e.g., language, type)
      - Sorting by time, like/dislike.

4. **Reactions and Comments:**
   - Handled by PUT/PATCH methods.

#### Notifications:
- Real-time notifications (if possible) or normal notifications.

#### Search API:
- **Filters:**
   - Language
- **Sort:**
   - Time
   - Like/Dislike

#### Additional APIs (Suggested):
- **User Snippets:**
   - API to fetch all snippets by a specific user.

- **Favorite Snippets:**
   - API to fetch or manage user-favorited snippets.

- **Recent Activity:**
   - API to fetch recent activities, e.g., new snippets, reactions, comments.
---

### Notes and references
#### [Snippet Manager Website Inspiation](https://snippetmater-early-testingdep.vercel.app/)
