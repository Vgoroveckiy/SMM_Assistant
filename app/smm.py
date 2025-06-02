from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import User
from config import openai_key
from generators.image_gen import ImageGenerator
from generators.text_gen import PostGenerator
from social_publishers.vk_publisher import VKPublisher
from social_stats.vk_stats import VKStats

smm_bp = Blueprint("smm", __name__)


@smm_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")


@smm_bp.route("/settings", methods=["GET", "POST"])
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.vk_api_id = request.form["vk_api_id"]
        user.vk_group_id = request.form["vk_group_id"]
        db.session.commit()
        flash("Settings saved!", "success")

    return render_template("settings.html", user=user)


@smm_bp.route("/post-generator", methods=["GET", "POST"])
def post_generator():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        tone = request.form["tone"]
        topic = request.form["topic"]
        generate_image = "generate_image" in request.form
        auto_post = "auto_post" in request.form

        user = User.query.get(session["user_id"])

        post_gen = PostGenerator(openai_key, tone, topic)
        post_content = post_gen.generate_post()

        image_url = None
        if generate_image:
            image_gen = ImageGenerator(openai_key)
            image_prompt = post_gen.generate_post_image_description()
            image_url = image_gen.generate_image(image_prompt)

        if auto_post:
            vk_publisher = VKPublisher(user.vk_api_id, user.vk_group_id)
            vk_publisher.publish_post(post_content, image_url)
            flash("Post published to VK successfully!", "success")

        return render_template(
            "post_generator.html", post_content=post_content, image_url=image_url
        )

    return render_template("post_generator.html")


@smm_bp.route("/vk-stats", methods=["GET"])
def vk_stats():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    vk_stats = VKStats(user.vk_api_id, user.vk_group_id)
    followers_count = vk_stats.get_followers()
    likes_and_views = vk_stats.get_likes_and_views(count=5)

    stats = {
        "Followers": followers_count,
        "Likes": likes_and_views[0]["likes"],
        "Views": likes_and_views[0]["views"],
        "Comments": "N/A",
        "Shares": "N/A",
    }

    return render_template("vk_stats.html", stats=stats)
