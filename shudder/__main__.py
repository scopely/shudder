"""Start the server and whatnot."""
import shudder.queue as queue


if __name__ == '__main__':
    conn, sqsq = queue.create_queue()
    sns_conn, sub = queue.subscribe_sns(sqsq)
    queue.death_row(sns_conn, conn, sqsq)
