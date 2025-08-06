# Chat Widget for Webflow

A modern, floating chat widget that embeds the Narcissus LangGraph chatbot into any Webflow website.

## Overview

This widget provides a sleek, floating chat interface that can be easily embedded into Webflow sites. The chatbot is powered by a LangGraph agent with custom tools and personality.

**Live Services:**
- **Chat Interface**: https://narcissus-ui.onrender.com 
- **API Backend**: https://narcissus-qi6m.onrender.com

## Features

- 🎨 **Modern Design** - Sleek floating chat button with smooth animations
- 📱 **Mobile Responsive** - Optimized for all screen sizes
- ⚡ **Performance** - Lazy-loads iframe only when needed
- 🎛️ **Customizable** - Easy to modify colors, text, and positioning
- 🔒 **Secure** - Hosted on Render with proper CSP headers
- 💫 **Smooth UX** - Bounce animations and hover effects

## Installation

### 1. Get the Code

Open `webflow-embed.html` and copy the entire contents (HTML, CSS, and JavaScript).

### 2. Add to Webflow

1. In Webflow Designer, drag a **Custom Code** element to your page
2. Paste the widget code into the element
3. **Important**: Set embed type to **"Inside Body"** 
4. Publish your site

### 3. Verify Installation

- Visit your published site
- Look for the purple chat bubble in the bottom-right corner
- Click to open the chat interface
- Send a test message

## Configuration

The widget comes pre-configured but can be customized:

```javascript
const CONFIG = {
    chatUrl: "https://narcissus-ui.onrender.com",
    title: "Ask me anything",
    brandColor: "#667eea"
};
```

## Files

- `webflow-embed.html` - Production-ready code for Webflow integration
- `chat-widget.html` - Standalone HTML file for local testing
- `README.md` - This documentation

## Customization

### Colors
Modify the gradient backgrounds in the CSS:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Header Text
Update the configuration:
```javascript
title: "Chat with our AI"
```

### Position
Move widget to the left side:
```css
.chat-widget {
    left: 20px;
    right: unset;
}
```

### Size
Adjust chat window dimensions:
```css
.chat-window {
    width: 400px;
    height: 700px;
}
```

## Local Testing

For testing before deploying to Webflow:

1. Open `chat-widget.html` in your browser
2. Click the chat bubble to test functionality
3. Verify the chat interface loads properly

## Troubleshooting

### Widget Not Visible
- Ensure Custom Code element is set to "Inside Body"
- Check that all code was copied from `webflow-embed.html`
- Clear browser cache and refresh

### Chat Interface Won't Load
- Open browser developer tools (F12) and check for console errors
- Verify the iframe attempts to load `https://narcissus-ui.onrender.com`
- Note: Services may take 30-60 seconds to wake up if idle

### Common Issues
- Mixed content errors: Ensure your Webflow site uses HTTPS
- CSP violations: The widget includes proper headers for iframe embedding
- JavaScript errors: Use only the provided `webflow-embed.html` code

## Technical Details

**Architecture:**
```
Webflow Site → Chat Widget → UI Service (iframe) → LangGraph API
```

**Technologies:**
- Frontend: Vanilla JavaScript, CSS3 animations
- Backend: LangGraph with FastAPI
- Deployment: Render.com hosting
- Integration: Iframe-based embedding with CSP compliance