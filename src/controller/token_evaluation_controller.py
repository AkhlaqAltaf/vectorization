from flask import jsonify, render_template


def token_evaluation_controller(request):

    data = [
        {
            "row": i + 1,
            "text_preview": f"Sample text {i + 1}....",
            "token_count": 5,
            "paragraph_count": 2,
            "tokens": ["token1", "token2", "token3", "token4", "token5"]
        }
        for i in range(17)
    ]
    return render_template('token_evaluation.html', data=data)