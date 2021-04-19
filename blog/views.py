from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {"allPosts":allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    post = Post.objects.get(slug=slug)
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]

        else:
            replyDict[reply.parent.sno].append(reply)

    print(replyDict)
    context = {"post":post, "comments":comments, "replyDict":replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postId = request.POST["postId"]
        post = Post.objects.get(postId=postId)
        CommentId = request.POST["CommentId"]

        if CommentId == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "your comment has been posted successfully.")

        else:
            parent = BlogComment.objects.get(sno=CommentId)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "your reply has been posted successfully.")
            
        return redirect(f"/blog/{post.slug}")
