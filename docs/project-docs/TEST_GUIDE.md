# Testing Guide

## Quick Test (File Protocol)

The simplest way to test right now:

1. **Open `index.html` directly** in your browser
   - Double-click `index.html` in File Explorer
   - Or right-click → "Open with" → Your browser
   - The file should open and display the homepage

2. **What to test**:
   - ✅ **Design**: Clean, minimal layout with good typography
   - ✅ **Theme Toggle**: Click the sun/moon icon in header (top right)
   - ✅ **Responsive**: Resize browser window to see mobile layout
   - ✅ **Navigation**: Click menu items (some links won't work yet - that's OK)
   - ✅ **Accessibility**: Try tabbing through the page with keyboard

## Better Test (Local Server)

For a proper test with all features working:

### Option 1: VS Code Live Server
1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"
4. Browser opens automatically at `http://127.0.0.1:5500`

### Option 2: Python HTTP Server
```bash
# If Python is installed:
python -m http.server 8000
# Then open: http://localhost:8000
```

### Option 3: Node.js (if installed)
```bash
npx serve .
# Then open the URL shown
```

### Option 4: PHP (if installed)
```bash
php -S localhost:8000
# Then open: http://localhost:8000
```

## What Should Work

✅ **Visual Design**:
- Clean, minimal aesthetic
- Generous whitespace
- System fonts (no external loading)
- Smooth transitions

✅ **Theme Toggle**:
- Click sun/moon icon in header
- Switches between light/dark mode
- Preference saved in browser

✅ **Responsive Design**:
- Resize browser to see mobile layout
- Mobile menu toggle (hamburger icon)
- Grid layouts adapt to screen size

✅ **Accessibility**:
- Skip-to-content link (press Tab on page load)
- Keyboard navigation (Tab through links)
- Focus states visible
- Semantic HTML structure

## What Won't Work Yet

⏳ **Missing Pages**:
- `/tours/` - Not generated yet
- `/about/` - Not generated yet
- `/contact.html` - Not generated yet
- Other pages - Need to be generated from scraped content

⏳ **Images**:
- No images yet (need to run image downloader)
- Placeholders will show broken images if referenced

⏳ **Real Content**:
- Currently using example content
- Need to scrape motorover.in for real data

## Testing Checklist

- [ ] Page loads without errors
- [ ] CSS styles apply correctly
- [ ] Theme toggle works (light/dark)
- [ ] Mobile navigation works (resize window)
- [ ] Keyboard navigation works (Tab key)
- [ ] No console errors (F12 → Console tab)
- [ ] Responsive design works (mobile/tablet/desktop)
- [ ] Skip-to-content link works (Tab on load)

## Browser Console Check

Press F12 to open DevTools, then check:

1. **Console Tab**: Should have no errors (warnings are OK)
2. **Network Tab**: 
   - `styles.css` should load (200 status)
   - `theme.js` and `main.js` should load
   - Any 404s are expected (missing pages/images)

## Next Steps After Testing

Once you've verified the design works:

1. **Install Python** (if not installed)
2. **Run scraper** to get real content
3. **Download images** from motorover.in
4. **Generate all pages** from templates
5. **Run Lighthouse** audit for performance scores

## Quick Fixes

If something doesn't work:

**CSS not loading?**
- Make sure you're using a local server (not file://)
- Check that `css/styles.css` exists

**JavaScript not working?**
- Check browser console (F12) for errors
- Make sure scripts are loading (Network tab)

**Theme toggle not working?**
- Check that `js/theme.js` exists
- Verify no JavaScript errors in console

**Mobile menu not working?**
- Check that `js/main.js` exists
- Verify JavaScript is enabled in browser
