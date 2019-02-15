import instaloader
import os
import etc

from datetime import datetime, timedelta


def scrape(profiles, export_directory, days=7, verbose=False):

    L = instaloader.Instaloader()

    expire_date = datetime.now() - timedelta(days=days)

    if verbose:
        profiles = etc.verbose_iter(profiles, 'Scanning insta profiles')

    pending_posts = []
    for profile in profiles:
        p = instaloader.Profile.from_username(L.context, profile)
        posts = p.get_posts()
        for post in posts:
            if verbose:
                print('.', end='')

            if post.date > expire_date:
                pending_posts.append(post)
            else:
                break

        if verbose:
            print('')

    if verbose:
        pending_posts = etc.verbose_iter(
            pending_posts, 'Downloading insta photos')

    for post in pending_posts:
        _, ext = os.path.splitext(post.url)
        etc.download_image_from_url(
            post.url, export_directory, post.shortcode + '.jpg')


if __name__ == '__main__':
    export_directory = etc.timestamp_directory(etc.find_desktop(), prefix='test')
    etc.create_directory(export_directory)

    scrape(['gamedev.inspo'], export_directory, verbose=True)