from flask import render_template_string

def chatinterface():
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Blog Generator</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">
            <style>
                body {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .input-group {
                    margin-bottom: 20px;
                }
                #topic {
                    width: 70%;
                    padding: 10px;
                    margin-right: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                button {
                    padding: 10px 20px;
                    background-color: #0066cc;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:disabled {
                    background-color: #cccccc;
                }
                .loading {
                    display: none;
                    margin: 20px 0;
                    color: #666;
                }
                .error {
                    color: #dc3545;
                    margin: 10px 0;
                }
                .result-section {
                    margin-top: 20px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 4px;
                }
                .markdown-body {
                    padding: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Blog Generator</h1>
                <div class="input-group">
                    <input type="text" id="topic" placeholder="Enter your blog topic" maxlength="200">
                    <button onclick="generateBlog()" id="generateBtn">Generate Blog</button>
                </div>
                <div class="loading" id="loadingIndicator">
                    Generating your blog content... Please wait...
                </div>
                <div id="result" class="markdown-body"></div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <script>
            function generateBlog() {
                const topic = $('#topic').val().trim();
                if (!topic) {
                    $('#result').html('<div class="error">Please enter a topic</div>');
                    return;
                }
                
                $('#generateBtn').prop('disabled', true);
                $('#loadingIndicator').show();
                $('#result').empty();
                
                $.ajax({
                    url: '/generate-blog',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ topic: topic }),
                    success: function(response) {
                        $('#result').html(`
                            <div class="result-section">
                                <h2>Outline</h2>
                                ${marked.parse(response.outline)}
                            </div>
                            <div class="result-section">
                                <h2>Final Blog Post</h2>
                                ${marked.parse(response.formatted_content)}
                            </div>
                        `);
                    },
                    error: function(error) {
                        $('#result').html(
                            '<div class="error">Error: ' + 
                            (error.responseJSON?.error || 'Failed to generate blog') + 
                            '</div>'
                        );
                    },
                    complete: function() {
                        $('#generateBtn').prop('disabled', false);
                        $('#loadingIndicator').hide();
                    }
                });
            }
            
            $('#topic').keypress(function(e) {
                if (e.which == 13) generateBlog();
            });
            </script>
        </body>
        </html>
        """)