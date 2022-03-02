
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <time.h>

// Section 88

__global__ void hello_cuda()
{
	printf("Hello CUDA!\n");
}

void section88()
{
	int nx = 16;
	int ny = 4;

	dim3 block(8, 2, 1);
	dim3 grid(nx/block.x, ny/block.y, 1);


	hello_cuda << <grid, block >> > ();
	cudaDeviceSynchronize();
	cudaDeviceReset();
}

// Section 89

__global__ void print_threadIds()
{
	printf("threadIdx.x:%d, threadIdx.y:%d, threadIdx.z:%d", 
		threadIdx.x, threadIdx.y, threadIdx.z);

}

// Section 90

__global__ void print_details()
{
	printf("-- blockDim.x:%d, blockDim.y:%d, blockDim.z:%d",
		blockDim.x, blockDim.y, blockDim.z);
	printf("-- gridDim.x:%d, gridDim.y:%d, gridDim.z:%d",
		gridDim.x, gridDim.y, gridDim.z);
}

void section89()
{
	int nx = 16;
	int ny = 16;
	dim3 block(8, 8);
	dim3 grid(nx/block.x, ny/block.y);
	print_threadIds << <grid, block >> > ();

	cudaDeviceSynchronize();
	cudaDeviceReset();
}

void section90()
{
	int nx = 16;
	int ny = 16;
	dim3 block(8, 8);
	dim3 grid(nx / block.x, ny / block.y);
	print_threadIds << <grid, block >> > ();

	cudaDeviceSynchronize();
	cudaDeviceReset();
}

//  Section 91

__global__ void unique_idx_calc_threadIdx(int* input)
{
	int tid = threadIdx.x;
	printf("threadIdx.x:%d, value:%d\n", tid, input[tid]);
}
__global__ void unique_gid_calculation(int* input)
{
	int tid = threadIdx.x;
	int offset = blockIdx.x * blockDim.x;
	int gid = tid + offset;
	printf("blockIdx.x:%d, threadIdx.x:%d, gid:%d, value:%d\n", 
		blockIdx.x, threadIdx.x, gid, input[gid]);
}


// Section 91

int section91_a()
{
	int array_size = 8;
	int array_byte_size = sizeof(int)*array_size;
	int h_data[] = {23, 9, 4, 53, 65, 12, 1, 33};

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(8);
	dim3 grid(1);

	unique_idx_calc_threadIdx << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}

int section91_b()
{
	int array_size = 8;
	int array_byte_size = sizeof(int) * array_size;
	int h_data[] = { 23, 9, 4, 53, 65, 12, 1, 33 };

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(4);
	dim3 grid(2);

	unique_idx_calc_threadIdx << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}

int section91_c()
{
	int array_size = 16;
	int array_byte_size = sizeof(int) * array_size;
	int h_data[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(4);
	dim3 grid(4);

	unique_gid_calculation << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}

// Section 92

__global__ void unique_gid_calculation_2d_a(int* input)
{
	int tid = threadIdx.x;
	int offset = blockIdx.x * blockDim.x;
	int gid = tid + offset;
	printf("blockIdx.x:%d, blockIdx.y:%d, threadIdx.x:%d, gid:%d, value:%d\n",
		blockIdx.x, blockIdx.y, tid, gid, input[gid]);
}

__global__ void unique_gid_calculation_2d_b(int* data)
{
	int tid = threadIdx.x;
	int block_offset = blockIdx.x * blockDim.x;
	int row_offset = blockDim.x * gridDim.x * blockIdx.y;
	int gid = row_offset + block_offset + tid;

	printf("blockIdx.x:%d, blockIdx.y:%d, threadIdx.x:%d, gid:%d, value:%d\n",
		blockIdx.x, blockIdx.y, tid, gid, data[gid]);
}

int section92_a()
{
	int array_size = 16;
	int array_byte_size = sizeof(int) * array_size;
	int h_data[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(4);
	dim3 grid(2, 2);

	unique_gid_calculation_2d_a << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}

int section92_b()
{
	int array_size = 16;
	int array_byte_size = sizeof(int) * array_size;
	int h_data[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(4);
	dim3 grid(2, 2);

	unique_gid_calculation_2d_b << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}

// Section 93

__global__ void unique_gid_calculation_2d_2d(int* data)
{
	int tid = blockDim.x * threadIdx.y + threadIdx.x;

	int num_threas_in_a_block = blockDim.x * blockDim.y;
	int block_offset = blockIdx.x * num_threas_in_a_block;

	int num_threads_in_a_row = num_threas_in_a_block * gridDim.x;
	int row_offset = num_threads_in_a_row * blockIdx.y;

	int gid = tid + block_offset + row_offset;


	printf("blockIdx.x:%d, blockIdx.y:%d, threadIdx.x:%d, gid:%d, value:%d\n",
		blockIdx.x, blockIdx.y, tid, gid, data[gid]);
}

int section93()
{
	int array_size = 16;
	int array_byte_size = sizeof(int) * array_size;
	int h_data[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 };

	for (int i = 0; i < array_size; i++)
	{
		printf("%d ", h_data[i]);
	}
	printf("\n \n ");

	int* d_data;
	cudaMalloc((void**)&d_data, array_byte_size);
	cudaMemcpy(d_data, h_data, array_byte_size, cudaMemcpyHostToDevice);

	dim3 block(2, 2);
	dim3 grid(2, 2);

	unique_gid_calculation_2d_2d << <grid, block >> > (d_data);
	cudaDeviceSynchronize();
	cudaDeviceReset();
	return 0;
}


// 95

__global__ void mem_trs_test(int* input)
{
	int gid = blockIdx.x * blockDim.x + threadIdx.x;
	printf("tid : %d, gid:%d, value:%d, \n", threadIdx.x, gid, input[gid]);
}

int section95()
{
	int size = 128;
	int byte_size = size * sizeof(int);
	int* h_input;
	h_input = (int*)malloc(byte_size);

	time_t t;
	srand((unsigned)time(&t));
	for (int i = 0; i < size; i++)
	{
		h_input[i] = (int)(rand() & 0xff);
	}
	int* d_input;
	cudaMalloc((void**)&d_input, byte_size);
	cudaMemcpy(d_input, h_input, byte_size, cudaMemcpyHostToDevice);

	dim3 block(64);
	dim3 grid(2);

	mem_trs_test << <grid, block >> > (d_input);
	cudaDeviceSynchronize();

	cudaFree(d_input);
	free(h_input);


	cudaDeviceReset();
	return 0;
}

int main()
{
	bool sec88 = false;
	bool sec89 = false;
	bool sec90 = false;
	bool sec91_a = false;
	bool sec91_b = false;
	bool sec91_c = false;
	bool sec92_a = false;
	bool sec92_b = false;
	bool sec93 = true;
	bool sec95 = true;

	if (sec88) section88();
	if (sec89) section89();
	if (sec90) section90();
	if (sec91_a) section91_a();
	if (sec91_b) section91_b();
	if (sec91_c) section91_c();
	if (sec92_a) section92_a();
	if (sec92_b) section92_b();
	if (sec93) section93();
	if (sec95) section95();

	for (int i = 0; i < 1000; i++)
	{
		section93();
	}

	return 0;
}
